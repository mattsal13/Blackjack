from blackjack_2 import *

num_decks = 4

## Create the shoe. 4 * num_decks of each rank--suit doesn't matter. (NEED TO RENAME THIS SHOE)
deck = dict()
for i in range(2, 11):
    deck[f'{i}'] = 4 * num_decks
deck['J'] , deck['Q'], deck['K'], deck['A'] = 4 * num_decks, 4 * num_decks, 4 * num_decks, 4 * num_decks

## See the bjfunctions file for all the functions that go into play_round(): this initiates a round of blackjack.
while deck_count(deck) > 26:
    play_round(deck)
    # For space
    for _ in range(3):
        print('.')
