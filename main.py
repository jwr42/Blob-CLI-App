"""
BLOB - the card game of prediction
Command Line Interface Card Game
"""

print("BLOB - THE CARD GAME OF PREDICTION\n")

# import dependencies
import numpy as np
import time

pause = 2 # time to pause between steps in seconds

time.sleep(pause)

# player parameters
num_players = 3
num_pots_in_round = 5  

# check if this is a valid combo
if num_players * num_pots_in_round > 52:
    NameError("Not enough cards in the deck!")

# establish the initial turn order
turn_order = [_ for _ in range(num_players)]

# cards are stored as tuples, first element represents suit and second element represents value
deck = [(suit, value) for suit in range(4) for value in range(13)]
hands = [] # for each player a list is added of the cards in their hands

#place x number of random cards from the deck into each player's hand
def get_hand(deck, num_pots_in_round):
    hand = []
    for i in range(num_pots_in_round):
        id = np.random.randint(len(deck))
        hand.append(deck[id])
        deck.pop(id)
    return hand

# get cards for each player
for player_id in turn_order:
    hands.append(get_hand(deck, num_pots_in_round))

# turn a tuple into a human readable string
def get_card_string(card_tuple):
    # 0 = Spade, 1 = Heart, 2 = Diamond, 3 = Clubs (unicode values for each used in the suit map)
    suit_map = {0:"\u2664", 1:"\u2661", 2:"\u2662", 3:"\u2667"}
    values_map = {0:"2", 1:"3", 2:"4", 3:"5", 4:"6", 5:"7", 6:"8", 7:"9", 8:"10", 9:"J", 10:"Q", 11:"K", 12:"A"}
    return values_map[card_tuple[1]]+suit_map[card_tuple[0]]

for player_id in turn_order:
    print(f"Player {player_id+1}'s cards: ", end="")
    for card_id in range(len(hands[player_id])):
        print(f"{get_card_string(hands[player_id][card_id])} ", end="")
    print() # jumps to a new line

# gather predictions from each of the players
predictions = []
print()
for player_id in turn_order:
    selection_id = input(f"Player {player_id+1}, please predict how many times you'll win this round: [enter a number] ")
    # check for non-integer values
    try:
        selection_id = int(selection_id)
    except ValueError:
        selection_id = np.random.randint(num_pots_in_round)
        print(f"Invalid entry, random choice of {selection_id} has been made instead - good luck!")
    if (selection_id < 0 or selection_id >= num_pots_in_round):
        selection_id = np.random.randint(num_pots_in_round)
        print(f"Invalid entry, random choice of {selection_id} has been made instead - good luck!")
    predictions.append(selection_id)

# store a count of the number of pots won, starting with a zero for every player
pots_won = {key:0 for key in range(num_players)}

for num_pot in range(num_pots_in_round):

    print()
    print(f"There are {num_pots_in_round - num_pot} pots left to win")
    print()
    
    # we skip for the first loop as they already know what cards they have
    if num_pot != 0:
        for player_id in turn_order:
            print(f"Player {player_id+1}'s cards: ", end="")
            for card_id in range(len(hands[player_id])):
                print(f"{get_card_string(hands[player_id][card_id])} ", end="")
            print() # jumps to a new line

    # create an empty list for players to add their cards to the plot
    pot = []

    for player_id in turn_order:

        must_follow_suit = False
        # Before asking a player for a card pick check if the player needs to follow suit 
        # (players must follow suit if they have a card in their hand matching the suit of the first card added to the pot)
        if len(hands[0]) > 1: # check if there's more than 1 card left in the players' hands
            player_suits = [x[0] for x in hands[player_id]] # list of suits in the player's hand
            if len(pot) > 0:
                pot_suit = pot[0][0] # suit set by the first card in the pot
                if pot_suit in player_suits:
                    must_follow_suit = True
                    valid_card_ids = []
                    print(f"Player {player_id+1}, you must follow suit therefore you may only select card number: ", end="")
                    for card_id in range(len(hands[player_id])):
                        if hands[player_id][card_id][0] == pot_suit:
                            print(f"{card_id+1}", end=" ")
                            valid_card_ids.append(card_id)
                    print()
        
        # If the player has only one card, play that card, otherwise ask which card the player would like to select
        if len(hands[player_id]) == 1:
            selection_id = 1
        else:
            selection_id = input(f"Player {player_id+1}, which card would you like to play? [enter a number corresponding to a card in your hand] ")

        # check for non-integer values
        try:
            selection_id = int(selection_id) - 1  # account for 0 indexing with the -1
        except ValueError:
            if must_follow_suit:
                selection_id = valid_card_ids[np.random.randint(len(valid_card_ids))]
            else:
                selection_id = np.random.randint(len(hands[player_id]))
            print("Invalid number entered, a random choice has been made instead")

        # check for integer values outside of the range
        if (selection_id < 0 or selection_id >= len(hands[player_id])):
            if must_follow_suit:
                selection_id = valid_card_ids[np.random.randint(len(valid_card_ids))]
            else:
                selection_id = np.random.randint(len(hands[player_id]))
            print("Invalid number entered, a random choice has been made instead")
        
        # check that the player has followed suit
        if must_follow_suit:
            if selection_id not in valid_card_ids:
                selection_id = valid_card_ids[np.random.randint(len(valid_card_ids))]
                print("Did not follow suit! A random valid card has been selected")
        
        # output the player card selection
        if len(hands[player_id]) > 1: # no need to announce of the final turn
            print(f"Player {player_id+1} selected {get_card_string(hands[player_id][selection_id])}")

        # add card from the player#s hand to the pot
        pot.append(hands[player_id][selection_id])
        hands[player_id].pop(selection_id)

    # return the cards that are in the pot for the players to see
    print()
    print(f"The cards in the pot are:", end=' ')
    for card_id in range(len(pot)):
            print(f"{get_card_string(pot[card_id])} ", end="")
    print() # provides a new line

     # by default the first card played wins    
    winning_card = pot[0]
    winning_card_id = 0
    for card_id in range(len(pot)):
        # if card has same suit but higher value, first card is beat
        if ((pot[card_id][0] == winning_card[0]) and (pot[card_id][1] > winning_card[1])):
            winning_card = pot[card_id]
            winning_card_id = card_id
        # if card has hearts as suit and winning card does not, first card is beat
        if ((pot[card_id][0] == 1) and (winning_card[0] != 1)):
            winning_card = pot[card_id]
            winning_card_id = card_id
        # if both cards have hearts as suit but card is higher value, first card is beat
        if ((pot[card_id][0] == 1) and (winning_card[0] == 1) and (pot[card_id][1] > winning_card[1])):
            winning_card = pot[card_id]
            winning_card_id = card_id
    
    # card position in the pot is determined by the turn order
    winning_player_id = turn_order[winning_card_id]
    print(f"Player {winning_player_id+1} wins the pot")

    # add win to the score counter dict
    pots_won[winning_player_id] += 1

    # pause before the next pot is created
    time.sleep(pause)

    # update the turn order TODO: update so that the player to win the round goes first
    turn_order.append(turn_order[0])
    turn_order.pop(0)

time.sleep(pause)
print()
for player_id in [_ for _ in range(num_players)]:
    print(f"Player {player_id+1} predicted they'd win {predictions[player_id]} and they won {pots_won[player_id]}")

time.sleep(pause)
print()
print("Thank you for playing Blob!")
print()