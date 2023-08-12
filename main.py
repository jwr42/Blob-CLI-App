"""
BLOB - card game of prediction
Command Line Interface Card Game
"""
# import dependencies
import numpy as np

# player parameters
num_players = 2
num_cards = 3

# check if this is a valid combo
if num_players * num_cards > 52:
    NameError("Not enough cards in the deck!")

# cards are stored as tuples, first element represents suit and second element represents value
deck = [(suit, value) for suit in range(4) for value in range(13)]
hands = [] # for each player a list is added of the cards in their hands

#place five random cards from the deck and place into a list
def get_hand(deck, num_cards):
    hand = []
    for i in range(num_cards):
        id = np.random.randint(len(deck))
        hand.append(deck[id])
        deck.pop(id)
    return hand

# get cards for each player
for i in range(num_players):
    hands.append(get_hand(deck, num_cards))

# unicode clubs: \u2667 hearts: \u2661 spades: \u2664 diamond: \u2662

# turn a tuple from into a human readable card

def get_card_string(card_tuple):
    # 0 = Spade, 1 = Heart, 2 = Diamond, 3 = Clubs
    suit_map = {0:"\u2664", 1:"\u2661", 2:"\u2662", 3:"\u2667"}
    values_map = {0:"2", 1:"3", 2:"4", 3:"5", 4:"6", 5:"7", 6:"8", 7:"9", 8:"10", 9:"J", 10:"Q", 11:"K", 12:"A"}
    return values_map[card_tuple[1]]+suit_map[card_tuple[0]]

for player_id in range(num_players):
    print(f"Player {player_id+1}'s cards: ", end='')
    for card_id in range(len(hands[player_id])):
        print(f"{get_card_string(hands[player_id][card_id])} ", end='')
    print() # jumps to a new line for the next player

# test for player one
selection_id = input(f"Player 1, which card would you like to play? [enter a number from 1 to {len(hands[0])}] ")

# check for non-integer values

try:
    selection_id = int(selection_id) - 1  # account for 0 indexing with the -1
except:
    selection_id = np.random.randint(len(hands[0]))
    print("Invalid number entered, a random choice has been made instead")

# check for integer values outside of the range

if selection_id < 0 or selection_id >= len(hands[0]):
    selection_id = np.random.randint(len(hands[0]))
    print("Invalid number entered, a random choice has been made instead")

# add card from the player to the pot

pot = []
pot.append(hands[0][selection_id])
hands[0].pop(selection_id)

print(f"Player 1 selected {get_card_string(pot[0])}")
print 

# select a card
# for player in range(num_players):
#     print("cards in hand:")
#     print(hands[player])
#     card_id = input("select a card index to play:")
#     card_id_int = int(card_id)
#     print(hands[player][card_id_int])
