import random


class Card:
    """Class defining a standard playing card"""

    def __init__(self, name, suit):
        """Creates valid playing cards

        Args:
            name (str|int): Integer or string name of the card's face value
            suit (str): One of the four valid standard suits

        Raises:
            InvalidValueError: For invalid values
            InvalidSuitError: For invalid suits

        Examples:
            >> Card('Ace', 'Spades')
            >> Card(6, 'Diamonds')
        """
        valid_suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        valid_values = ['Ace', '2', '3', '4', '5', '6',
                        '7', '8', '9', '10', 'Jack', 'Queen', 'King',
                        2, 3, 4, 5, 6, 7, 8, 9, 10]

        if name not in valid_values:
            raise InvalidValueError("Not a valid card value")

        if suit not in valid_suits:
            raise InvalidSuitError("Not a valid suit value")

        self._name = str(name)
        self._suit = str(suit)

        try:
            self._value = int(name)
        except ValueError:
            if name == 'Ace':
                self._value = 1
            else:
                self._value = 10

    @property
    def value(self):
        """Returns an integer, blackjack-style, face-value of the card"""
        return self._value

    def __str__(self):
        """String representation of the card"""
        return f"{self._name} of {self._suit}"

    def __repr__(self):
        """Same as __str__"""
        return str(self)


class Deck:

    def __init__(self):
        """Creates a standard 52-card deck"""
        values = ['Ace', '2', '3', '4', '5', '6', '7',
                  '8', '9', '10', 'Jack', 'Queen', 'King']
        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        self._cards = []

        for s in suits:
            for v in values:
                self._cards.append(Card(v, s))

    def __len__(self):
        """The current length of the deck"""
        return len(self._cards)

    def __iter__(self):
        """Iterates over all cards in a deck"""
        return iter(self._cards)

    @property
    def cards(self):
        """Provides readonly access to the cards list"""
        return self._cards

    def shuffle(self):
        """Randomizes the deck"""
        random.shuffle(self._cards)

    def draw(self, n=1):
        """Draws a specified number of cards

        Args:
            n (int): Number of cards to draw

        Returns:
            A list of cards, always a list even when n=1

        Raises:
            EmptyDeckError: When attempting to draw more cards than remain
        """
        if len(self) < n:
            raise EmptyDeckError("Not enough cards left to draw")

        cards = []
        for x in range(n):
            cards.append(self._cards.pop())

        return cards


class EmptyDeckError(Exception):
    """Raised when attempting to draw on an empty deck"""
    pass


class InvalidValueError(Exception):
    """Raised when creating a card with an invalid value"""
    pass


class InvalidSuitError(Exception):
    """Raised when creating a card with an invalid suit"""
    pass
