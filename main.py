"""
BLOB - card game of prediction
"""

import numpy as np


# cards are stored as tuples, first element represents suit and second element represents value
deck = [(suit, value) for suit in range(4) for value in range(13)]

"""
card_id = np.random.randint(len(deck))
print(deck[card_id])
"""

num_players = 2

hands = [[] for _ in range(num_players)]

print(hands)

#place five random cards from the deck and place into a list
def get_hand(deck):
    hand = []
    for i in range(5):
        id = np.random.randint(len(deck))
        hand.append(deck[id])
        deck.pop(id)
    return hand

# get cards for each player
for i in range(num_players):
    hands[i].append(get_hand(deck))

# select a card
for player in range(num_players):
    print("cards in hand:")
    print(hands[player])
    card_id = input("select a card index to play:")
    card_id_int = int(card_id)
    print(hands[player][card_id_int])

print(hands)
