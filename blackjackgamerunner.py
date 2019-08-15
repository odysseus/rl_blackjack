from blackjackgame import BlackjackGame


class BlackjackGameRunner:

    def __init__(self):
        """Creates a game runner object"""
        self.game = BlackjackGame()

    def run(self, responder, n=-1):
        """Runs the game using the responder function as the 'Player'

        Loops infinitely until it receives an 'End' response from the responder

        Args:
            responder:  A function that responds with the necessary strings
                        based on the game state passed to it.
            n:          Number of hands, for an infinite number of hands
                        use any negative integer.

        Responses:
            When game is active:
                - 'Hit': If player busts the game switches to not active
                - 'Stand':  Game switches to not active, dealer hits until it
                            reaches 17 or more and then returns the outcome
                            of the hand.
            When game is not active (player has busted or stood):
                - 'Deal': Deals another hand, game switches to active
                - 'End': Ends the game without another hand. Method returns

        Raises:
            InvalidActionError: When an improper response is given
        """
        while n != 0:
            self.game.deal()

            while self.game.active:
                # Deal with hitting until bust or stand
                response = responder(self.game.state())

                if response == "hit":
                    self.game.player_hit()
                elif response == "stand":
                    self.game.player_stand()
                else:
                    raise InvalidActionError(
                        "Valid actions are 'Hit' or 'Stand'")

            # Deal with end of hand stuff, print totals, etc.
            if self.game.player_bust:
                response = responder(self.game.state())
            else:
                while self.game.dealer_total < 17:
                    self.game.dealer_hit()

                response = responder(self.game.state())

            if response == 'end':
                return None

            n -= 1



class InvalidActionError(Exception):
    """Raised when an un-parseable action is received by the game runner"""
    pass
