import random

## The dictionary of card values
card_values = dict()
# Add the number values
for i in range(2, 11):
    card_values[f'{i}'] = i
# And the face values
card_values['J'], card_values['Q'], card_values['K'] = 10, 10, 10
# Ace will initially count as 11. If the tally runs over 21, then 10 will be subtracted ONCE for EACH ace already in the hand.
card_values['A'], card_values['A2'] = 11, 1

## Cards remaining in the deck.
def deck_count(deck):
    return sum(deck[rank] for rank in deck)

## We will need a function to create a hand for the player when needed.
def create_hand(deck, player_hands):
    new_hand = dict()
    # Initialize
    for rank in deck:
        new_hand[rank] = 0
    new_hand['A2'] = 0
    # Add it to the list of hands.
    player_hands.append(new_hand)  

## Get the numerical value of EACH hand in player_hands. This will be used to update the draw in case of Ace overdraw, and return on busts. 
def get_player_count(hand_num, player_hands):
    return sum(player_hands[hand_num][rank] * card_values[rank] for rank in player_hands[hand_num]) 

def get_dealer_count(dealer_hand):
    return sum(dealer_hand[rank] * card_values[rank] for rank in dealer_hand)

## This deals a card to the hand_num'th card. We need this to update player_hands[hand_num].
def player_draw(hand_num, player_hands, deck):
    ranks = list(deck.keys())
    # We have to make sure the random card is actually in the deck. For all intents and purposes, deck_count() > 0 
    # should always be True, but better not to have a potential inf loop in the program.
    while deck_count(deck) > 0:
        random_draw = random.choice(ranks)
        if deck[random_draw] > 0:
            break
        else:
            continue
    # Update the deck with the draw.
    deck[random_draw] -= 1
    # Add new draw to hand_num'th hand and append to draws.
    player_hands[hand_num][random_draw] += 1
    # If Ace overdraw then change the value of the A from 11 to 1 and update the player's hand. 
    while get_player_count(hand_num, player_hands) > 21 and player_hands[hand_num]['A'] > 0:
        player_hands[hand_num]['A'] -= 1
        player_hands[hand_num]['A2'] += 1

    return random_draw

## Dealer only has on hand so this part is straightforward.
def dealer_draw(dealer_hand, deck):
    ranks = list(deck.keys())
    # Draw a random card from the deck. 
    random_draw = random.choice(ranks)
    # Update the deck with the draw.
    deck[random_draw] -= 1
    # Update the dealer's hand.
    dealer_hand[random_draw] += 1
    # If Ace overdraw then change the value of the A from 11 to 1 and update dealer's hand.
    while get_dealer_count(dealer_hand) > 21 and dealer_hand['A'] > 0:
        dealer_hand['A'] -= 1
        dealer_hand['A2'] += 1

    return random_draw

## Splitting prompt.
def split(pair_card, player_hands, player_ranks, deck):
    inp = input("Split your pair? (y/n) ")
    if inp == 'y':
        # Create a new hand which updates player_hands. Make sure to update the original hand
        # because we are now removing one of the cards from it.
        create_hand(deck, player_hands)
        player_hands[0][pair_card] -= 1
        player_hands[1][pair_card] += 1
        # Create a new list in player_ranks for viewing the hands.
        player_ranks.append([player_ranks[0].pop(0)])
        # Deal the new cards
        player_ranks[0].append(player_draw(0, player_hands, deck))
        player_ranks[1].append(player_draw(1, player_hands, deck))
        # Print both hands for the user to see.
        print(player_ranks)
    elif inp == 'n':
        return
    else:
        # Re-prompt the user if they enter something other than y or n.
        split(pair_card, player_hands, player_ranks, deck)

## Prompts the user to hit or stay on hand_num. Recall the form player_draw(hand_num, player_hands, deck)
def hit_stay(hand_num, player_ranks, player_hands, deck):
    inp = input(f"Hit, stay or double down on hand {hand_num}? (h/s/d) ")
    if inp == 'h':
        new_card = player_draw(hand_num, player_hands, deck)
        player_ranks[hand_num].append(new_card)
        print(player_ranks)
        if get_player_count(hand_num, player_hands) > 21:
            return
        else:
            hit_stay(hand_num, player_ranks, player_hands, deck)
    # Remeber that there is no hitting after doubling. 
    elif inp == 'd':
        new_card = player_draw(hand_num, player_hands, deck)
        # The * is to indicate that the player has doubled down on this card. 
        player_ranks[hand_num].append(new_card + '*')
        print(player_ranks)
    elif inp == 's':
        return
    # If the user enters anything but h, s, or d. 
    else:
        hit_stay(hand_num, player_ranks, player_hands, deck) 

## NOTE: DEALER MUST GO AFTER PLAYER. We will simulate no hit on soft 17 for now to keep things simple.
def dealer_turn(dealer_ranks, dealer_hand, deck):
    while get_dealer_count(dealer_hand) < 17:
        new_card = dealer_draw(dealer_hand, deck)
        dealer_ranks.append(new_card)

## Initiates a round of blackjack.
def play_round(deck):
    ## Dictionaries encoding what cards the dealer and player currently hold. The dealer only ever has one hand, so this part is straightforward. 
    dealer_hand = dict()
    for rank in deck:
        dealer_hand[rank] = 0
    # Add in so-called A2 rank, for when an ace is counted as 1 instead of 11. 
    dealer_hand['A2'] = 0

    ## The player can have multiple hands, so this will be a LIST of DICTs.
    player_hands = list()

    ## Deal the first card to the dealer. Order doesn't matter here since all is random anyway.
    ## It does matter however that the remaining dealer draws come AFTER the player.
    dealer_ranks = []
    dealer_up_card = dealer_draw(dealer_hand, deck)
    dealer_ranks.append(dealer_up_card)

    ## Start off the round.
    print("Dealer's up card: " + dealer_up_card)

    ## Initialize. Start by creating hand 0 for the player.
    create_hand(deck, player_hands)

    ## This is for printing mainly. Note it will be a LIST of LISTs, to keep track of potentially multiple hands.
    player_ranks = [[]]
    # Remember that player_draw(hand_num, player_hands, deck) both updates the player_hand DICT but returns the LIST of draws. 
    # Draw 2 cards to hand 0.
    player_ranks[0].append(player_draw(0, player_hands, deck))
    player_ranks[0].append(player_draw(0, player_hands, deck))
    # Print for the user to see their first two cards.
    print(player_ranks)

    # Conditional for splitting prompt
    if player_ranks[0][0] == player_ranks[0][1]:
        pair_card = player_ranks[0][0]
        split(pair_card, player_hands, player_ranks, deck)

    ## Now prompt the player for cards.
    for i in range(len(player_hands)):
        hit_stay(i, player_ranks, player_hands, deck)

    ## Dealer's turn if there is at least one hand in player_hands that is not a bust. Run a loop to check for this.
    totally_busted = True
    pointer = 0
    while pointer < len(player_hands) and totally_busted is True:
        if get_player_count(pointer, player_hands) < 22:
            totally_busted = False
        else:
            pointer += 1

    ## The dealer takes his turn if the player has not busted on all hands.
    if not totally_busted:
        dealer_turn(dealer_ranks, dealer_hand, deck)

    ## Evaluations. 
    # Dealer's cards + value.
    print(f"Dealer's cards: {dealer_ranks} --> {get_dealer_count(dealer_hand)}")
    # Player's cards. 
    for i in range(len(player_hands)):
        print(f"Your cards: {player_ranks[i]} --> {get_player_count(i, player_hands)}")

        if get_player_count(i, player_hands) > 21:
            print(f"Busted! You lose hand {i}.")
        else:
            # Player has not busted at this point, so compare to the dealer's cards.
            # If both the player and dealer bust, then the player loses. 
            if get_dealer_count(dealer_hand) > 21:
                print(f"Dealer busted. You win hand {i}.")
            else:
                if get_player_count(i, player_hands) > get_dealer_count(dealer_hand):
                    print(f"You win hand {i}.")
                elif get_player_count(i, player_hands) < get_dealer_count(dealer_hand):
                    print(f"You lose hand {i}.")
                else:
                    print("Push.")
