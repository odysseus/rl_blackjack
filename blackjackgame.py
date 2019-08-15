from deck import *


class Hand:
    """A list of cards representing a single hand in blackjack"""

    def __init__(self, cards=[]):
        """Initializes the cards list"""
        self._cards = cards
        self._soft = False

    def __str__(self):
        """The string representation of the list and contained cards"""
        return str(self._cards)

    def __repr__(self):
        """Same as __str__"""
        return str(self)

    def __len__(self):
        """Length of the cards list"""
        return len(self._cards)

    def __iter__(self):
        """Iterator over the cards list"""
        return iter(self._cards)

    def __add__(self, other):
        """Add a card or cards to the hand using `+`

        Args:
            other:  The cards to add, can be either an array of Card objects,
                    a Hand object, or a single Card

        Raises:
            TypeError: When `other` is an invalid type
        """
        if type(other) == list:
            self._cards = self._cards + other
        elif type(other) == Hand:
            self._cards = self._cards + other._cards
        elif type(other) == Card:
            self._cards.append(other)
        else:
            raise TypeError("Invalid type for <Hand> + <Type>")

    @property
    def contains_ace(self):
        """Returns True if the hand contains an Ace"""
        for card in self:
            if card.value == 1:
                return True
        return False

    @property
    def soft(self):
        """Checks the current total and returns True on soft totals
        A soft total is an Ace being counted as 11 but could count as 1
        """
        self.total
        return self._soft

    @property
    def cards(self):
        """Readonly access to the cards list"""
        return self._cards

    @property
    def total(self):
        """Returns the (Blackjack) total for the hand
        Aces are handled automatically
        """
        total = 0
        for card in self._cards:
            total += card.value

        if total <= 11 and self.contains_ace:
            self._soft = True
            return total + 10
        else:
            self._soft = False
            return total

    @property
    def bust(self):
        """True if the hand total is > 21"""
        return self.total > 21


class BlackjackGame:

    def __init__(self):
        """Creates a game with a deck, one player, and dealer"""
        self._deck = Deck()
        self._deck.shuffle()
        self._dealer = Hand()
        self._player = Hand()
        self._player_standing = False
        self._prevstate = None

    @property
    def dealer(self):
        """Readonly access to the dealer's hand"""
        return self._dealer

    @property
    def player(self):
        """Readonly access to the player's hand"""
        return self._player

    @property
    def active(self):
        """Returns True if the player can still choose to Hit"""
        return (not self.player_standing and not self.player_bust)

    @property
    def player_standing(self):
        """True if the player has chosen to stand during the current hand"""
        return self._player_standing

    @property
    def dealer_upcard(self):
        """Returns the face value of the dealer's upcard"""
        upcard = self.dealer.cards[0].value
        if upcard == 1:
            return 11
        else:
            return upcard

    @property
    def dealer_total(self):
        """Returns the dealer's total hand value"""
        return self.dealer.total

    @property
    def player_total(self):
        """Returns the player's total hand value"""
        return self.player.total

    @property
    def player_bust(self):
        """True if the player has busted"""
        return self.player.bust

    @property
    def dealer_bust(self):
        """True if the dealer has busted"""
        return self.dealer.bust

    @property
    def prevstate(self):
        return self._prevstate

    def prevstate_tup(self, action):
        """Returns a string summarizing the previous state
        The information is from the player's perspective so includes only the
        players hand total and dealer's upcard, along with the action chosen.

        self._prevstate will be None on new hands where the player has not
        chosen an action (setting to None is handled in self.deal())

        Args:
            action: The action chosen, either 'Hit' or 'Stand'

        EG: 'S17-8 Hit'-- Player had a soft 17, dealer upcard was 8,
            player chose to hit
        """
        soft = 'S' if self.player.soft else 'H'
        return (f"{soft}{self.player_total}-{self.dealer_upcard}", action)

    def deal(self):
        """Removes old hands and deals new ones"""
        self._prevstate = None
        self._player_standing = False
        self._dealer = Hand(self.safe_draw(2))
        self._player = Hand(self.safe_draw(2))

    def safe_draw(self, n):
        """Draws cards without raising an EmptyDeckError

        If not enough cards remain to be drawn, creates and shuffles a
        new deck before drawing.

        Args:
            n: Number of cards to draw

        Returns:
            A list of Card objects
        """
        cards = []
        try:
            cards = self._deck.draw(n)
        except EmptyDeckError:
            self._deck = Deck()
            self._deck.shuffle()
            cards = self._deck.draw(n)
        return cards

    def player_hit(self):
        """Adds one card to the players hand from the top of the deck"""
        self._prevstate = self.prevstate_tup('hit')
        self.player + self.safe_draw(1)

    def dealer_hit(self):
        """Adds one card to the dealer's hand from the top of the deck"""
        self.dealer + self.safe_draw(1)

    def player_stand(self):
        """Action method used when the player chooses to stand"""
        self._prevstate = self.prevstate_tup('stand')
        self._player_standing = True

    def outcome_str(self):
        """Returns a string describing the outcome ['Win'|'Loss'|'Push']"""
        if not self.player_bust and self.player_total > self.dealer_total:
            return "Win"
        elif not self.player_bust and self.dealer_bust:
            return "Win"
        elif self.player_total == self.dealer_total:
            return "Push"
        else:
            return "Loss"

    def outcome_descr(self):
        """Describes the outcome in more detail
        For 'Win' mentions whether this is a result of the dealer busting
        or the player having a higher total. For 'Loss' whether the player
        busted or the dealer had a higher total.
        """
        outcome = self.outcome_str()
        if outcome == 'Win':
            if self.dealer_bust:
                return 'Dealer busted'
            else:
                return 'Player won'
        elif outcome == 'Loss':
            if self.player_bust:
                return 'Player busted'
            else:
                return 'Dealer won'
        else:
            return 'Tie'

    def state(self):
        """Returns a dictionary with the current state of the game

        Different keys are returned depending on whether the game is 'active',
        ie: The player still has decisions to make, versus 'not active' where
        the player has either busted or chosen to stand. When called on a
        'not active' game it returns the outcome (Win|Push|Loss) as well as a
        more detailed description of the outcome (eg: 'Player busted')
        """
        state = {}

        if self.active:
            state["active"] = True
            state["player_total"] = self.player_total
            state["dealer_upcard"] = self.dealer_upcard
            state['player_soft'] = self.player.soft
            state['dealer_soft'] = self.dealer.soft
            state['prevstate'] = self.prevstate
        else:
            state["active"] = False
            state["player_total"] = self.player_total
            state["dealer_total"] = self.dealer_total
            state["player_bust"] = self.player_bust
            state["dealer_bust"] = self.dealer_bust
            state['prevstate'] = self.prevstate

            state["outcome"] = self.outcome_str()
            state["description"] = self.outcome_descr()

        return state
