from uu import Error
from random import shuffle

# builds a dict of cards
def build_deck():

    # creates dict with key being suit type
    suits = {'Hearts':list(),
             'Spades':list(),
             'Clubs':list(),
             'Dimonds':list()}

    #creating the correct values
    value = list(range(2,11))
    # chaging value to be strings
    value = [str(x) for x in value]
    #adding in non numerical values
    value.extend(('Ace', 'King', 'Queen', 'Jack'))
    #adding the list of values to the key
    for k in suits:
        suits[k].extend(value)
    return suits

# takes a dict of cards of primary cards and discarded cards, adds together and shuffles, checking for remaining card count
def shuffle_cards(primary, discard = False):
    # raising error if incorrect paramater added to primary
    if isinstance(primary, dict):
        #creating empty list for the outputted list
        shuffled_deck = list()

        #changing dict in to the list
        for key, values in primary.items():
            for value in values:
                shuffled_deck.append(f'{value} of {key}')
        # checking list is correct size
        if len(shuffled_deck) != 52:
            raise Error(f'Length of deck not 52 but | {len(shuffled_deck)} |')
    elif isinstance(primary, list):
        shuffled_deck = primary
    else:
        raise Error(f'Primary should be type dict or list. But type {type(primary)}')



    # if discard added, adds to the shuffled deck
    if isinstance(discard, list):
        print(f'leng of shuffled {len(shuffled_deck)}')
        print(f'len of discard {len(discard)}')
        shuffled_deck.extend(discard)
        print(f'result from adding shfulled list and sicard {len(shuffled_deck)}')

    shuffle(shuffled_deck)
    return shuffled_deck

def draw_card(hand, deck, discard_pile, start=False, ai=False):
    if start == True:
        if len(deck) < 4:
            deck = shuffle_cards(primary=deck, discard=discard_pile)
            discard_pile = list()
        draw = deck[:2]
        hand.extend(draw)
        del deck[0:2]
        draw = deck[:2]
        ai.extend(draw)
        del deck[0:2]
        return  hand, deck, discard_pile, ai_hand

    else:
        if len(deck) < 1:
            deck = shuffle_cards(primary=deck, discard=discard_pile)
            discard_pile = list()
        draw = deck[0:1]
        hand.extend(draw)
        del deck[0:1]

    return hand, deck, discard_pile

def hand_value(hand):
    aces = 0
    values = [c[:2] for c in hand]
    values = [x.replace(" ", "") for x in values]

    for x in values:
        if x in ['Ki', 'Qu', 'Ja']:
            values.remove(x)
            values.insert(0 ,10)
        elif x == 'Ac':
            aces = aces + 1
            values.remove(x)
            values.insert(0, 0)

    values = [int(x) for x in values]
    if aces == 0:
        return  sum(values)
    else:
        ones = 0
        for x in range(aces):
            value = sum(values) + (11 * aces) + ones
            if value <= 21:
                return value
            else:
                ones = ones + 1
                aces = aces - 1
                if aces <= 0:
                    value = sum(values) + ones
                    return value

def carry_on(con):

    check = False
    while check == False:
        try:
            con = con[0].lower()
        except IndexError:
            con = con
        if con == 'y':
            return True
        elif con == 'n':
            return False
        else:
            con = input("Please, just yes or no. ")

def play_again():
    con = input('Do you want to play again? ')
    outcome = carry_on(con)
    return outcome

def easy_ai(hand,deck, discard):
    value = hand_value(hand)
    while value < 14:
        hand, deck, discard = draw_card(hand=hand, deck=deck, discard_pile=discard)
        value = hand_value(hand)
    return hand, deck, discard


main_deck = build_deck()


shuffled_deck = shuffle_cards(primary=main_deck)

discard_pile = list()

player_hand = list()

ai_hand = list()

player_win = 0
ai_win = 0

print("Welcome to blackjack")

con = input('Do you want to play? ')

play = carry_on(con)

if con:
    print('Lets go!')
else:
    print('That\'s too bad')

while play:
    player_hand, shuffled_deck, discard_pile, ai_hand = draw_card(hand=player_hand, deck=shuffled_deck, discard_pile=discard_pile, start=True, ai=ai_hand)

    print(f'Your hand is {player_hand}')
    ai_hand, shuffled_deck, discard_pile = easy_ai(ai_hand, shuffled_deck, discard_pile)
    print(f'Your opponent hand is: {ai_hand}')
    blackjack = False
    ai_value = hand_value(ai_hand)
    player_value = hand_value(player_hand)
    if ai_value > 21:
        print('Opponent went bust, you win!')
        blackjack = True
        player_win +=1

    if (player_value == 21 and len(player_hand) == 2) or (ai_value == 21 and len(ai_hand) == 2):
        if (ai_value == 21 and len(ai_hand) == 2) and (player_value == 21 and len(player_hand) == 2):
            print('Both players BlackJack, what are the chances!')
            blackjack = True
        elif (ai_value == 21 and len(ai_hand) == 2):
            print('Opponent has BlackJack, you loose')
            blackjack=True
            ai_win +=1
        else:
            print('BlackJack you win!')
            blackjack = True
            player_win +=1

    if not blackjack:
        hit = input('Do you want to hit? ')
        stay_stand = carry_on(hit)
        while stay_stand:
            if stay_stand:

                player_hand, deck, discard_pile = draw_card(player_hand, shuffled_deck, discard_pile=discard_pile)
                print(f'Your new hand is {player_hand}')
            value = hand_value(player_hand)
            if value > 21:
                print(f'You went bust your total is {value}')
                stay_stand = False
            else:
                hit = input('Do you want to hit? ')
                stay_stand = carry_on(hit)

    player_value = hand_value(player_hand)

    if player_value > 21:
        print('You loose!')
        ai_win +=1
    elif ai_value == player_value:
        print(f'Your card value is {player_value} your opponent\'s is {ai_value}.')
        print('It\'s a draw!')
    elif ai_value > player_value:
        print(f'Your card value is {player_value} your opponent\'s is {ai_value}.')
        print('You loose!')
        ai_win +=1
    elif player_value > ai_value:
        print(f'Your card value is {player_value} your opponent\'s is {ai_value}.')
        print('You win')
        player_win +=1
    else:
        raise Error(f'No win condition found. {player_value}, {ai_value}')


    print()
    print()
    print()

    discard_pile.extend(player_hand + ai_hand)

    player_hand.clear()
    ai_hand.clear()
    print(f'You have won {player_win} times.')
    print(f'Your opponent has won {ai_win} times')
    play = play_again()