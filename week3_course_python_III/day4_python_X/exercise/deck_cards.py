
def deck_builder():
    count = 1
    deck_of_cards = []
    suits = ['hearts', 'spades', 'clubs', 'diamonds']

    while count < 13:
        for i in suits:
            deck_of_cards.append(str(count) + '_' + i)

        count += 1

    return deck_of_cards