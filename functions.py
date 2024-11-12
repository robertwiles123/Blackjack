from uu import Error


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

def draw_card(hand, deck, discard_pile, start=False, ai=None):
    if start:
        if len(deck) < 4:
            deck = shuffle_cards(primary=deck, discard=discard_pile)
            discard_pile = list()

        draw = deck[:2]
        hand.extend(draw)
        del deck[0:2]

        # Ensure `ai` is defined to receive cards
        if ai is not None:
            draw = deck[:2]
            ai.extend(draw)
            del deck[0:2]


        return hand, deck, discard_pile, ai

    else:
        if len(deck) < 1:
            deck = shuffle_cards(primary=deck, discard=discard_pile)
            discard_pile = list()

        draw = deck[:1]
        hand.extend(draw)
        del deck[0:1]

    return hand, deck, discard_pile
