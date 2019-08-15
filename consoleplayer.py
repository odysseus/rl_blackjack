from blackjackgamerunner import BlackjackGameRunner


class ConsolePlayer:

    def __init__(self):
        """Creates the game runner object"""
        self.game = BlackjackGameRunner()

    def run(self):
        """Runs the interactive console game"""
        self.game.run(self.consolerun)

    def consolerun(self, state):
        """Responder function for an interactive console blackjack game"""
        hit_strings = ['h', 'H', 'hit', 'Hit']
        stand_strings = ['s', 'S', 'stand', 'Stand']
        end_strings = ['e', 'E', 'end', 'End', 'x', 'X']

        if state['active']:
            print("""
Player Total:  {player_total} Soft: {player_soft}
Dealer Upcard: {dealer_upcard}

Choose [H]it or [S]tand:
                """.format(**state))
            response = input()

            if response in hit_strings:
                return 'hit'
            elif response in stand_strings:
                return 'stand'

        else:
            print("""
---Result---
Player Total: {player_total}
Dealer Total: {dealer_total}
{outcome} - {description}

Type [E]nd to stop or ENTER to continue
            """.format(**state))

        response = input()
        if response in end_strings:
            return 'end'
        else:
            return None

    def singlerun(self, state):
        """Runs a single, fully automated hand

        Primarily to confirm that states are being passed correctly.
        """
        if state['active']:
            print(state)
            if state['player_total'] < 17:
                return 'hit'
            else:
                return 'stand'
        else:
            print(state)
            return 'end'


game = ConsolePlayer()
game.run()
