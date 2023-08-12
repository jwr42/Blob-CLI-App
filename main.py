"""
BLOB - card game of prediction
Command Line Interface Card Game
"""
# import dependencies
import numpy as np

# player parameters
num_players = 2
num_cards_in_round = 3

# check if this is a valid combo
if num_players * num_cards_in_round > 52:
    NameError("Not enough cards in the deck!")

# cards are stored as tuples, first element represents suit and second element represents value
deck = [(suit, value) for suit in range(4) for value in range(13)]
hands = [] # for each player a list is added of the cards in their hands

#place five random cards from the deck and place into a list
def get_hand(deck, num_cards_in_round):
    hand = []
    for i in range(num_cards_in_round):
        id = np.random.randint(len(deck))
        hand.append(deck[id])
        deck.pop(id)
    return hand

# get cards for each player
for i in range(num_players):
    hands.append(get_hand(deck, num_cards_in_round))

# turn a tuple into a human readable string
def get_card_string(card_tuple):
    # 0 = Spade, 1 = Heart, 2 = Diamond, 3 = Clubs (unicode values for each used in the suit map)
    suit_map = {0:"\u2664", 1:"\u2661", 2:"\u2662", 3:"\u2667"}
    values_map = {0:"2", 1:"3", 2:"4", 3:"5", 4:"6", 5:"7", 6:"8", 7:"9", 8:"10", 9:"J", 10:"Q", 11:"K", 12:"A"}
    return values_map[card_tuple[1]]+suit_map[card_tuple[0]]

for player_id in range(num_players):
    print(f"Player {player_id+1}'s cards: ", end='')
    for card_id in range(len(hands[player_id])):
        print(f"{get_card_string(hands[player_id][card_id])} ", end='')
    print() # jumps to a new line for the next player

# create an empty list for players to add their cards to the plot
pot = []

# TODO: add the follow suit rule!!!
for player_id in range(num_players):

    # ask which card the player would like to select
    selection_id = input(f"Player {player_id+1}, which card would you like to play? [enter a number from 1 to {len(hands[player_id])}] ")

    # check for non-integer values
    try:
        selection_id = int(selection_id) - 1  # account for 0 indexing with the -1
    except:
        selection_id = np.random.randint(len(hands[player_id]))
        print("Invalid number entered, a random choice has been made instead")

    # check for integer values outside of the range
    if selection_id < 0 or selection_id >= len(hands[player_id]):
        selection_id = np.random.randint(len(hands[player_id]))
        print("Invalid number entered, a random choice has been made instead")

    # add card from the player to the pot
    pot.append(hands[player_id][selection_id])
    hands[player_id].pop(selection_id)

    # output the player card selection
    print(f"Player {player_id+1} selected {get_card_string(pot[player_id])}")

# return the carrds that are in the pot for the players to see
print(f"The cards in the pot are:", end=' ')
for card_id in range(len(pot)):
        print(f"{get_card_string(pot[card_id])} ", end='')
