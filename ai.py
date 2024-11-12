import functions

def easy_ai(hand,deck, discard):
    value = functions.hand_value(hand)
    while value < 14:
        hand, deck, discard = functions.draw_card(hand=hand, deck=deck, discard_pile=discard)
        value = functions.hand_value(hand)
    return hand, deck, discard