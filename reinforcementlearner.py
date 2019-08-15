from blackjackgamerunner import BlackjackGameRunner
import random


class ScoreTally:

    def __init__(self):
        """Initializes a score tally"""
        self._score = 0
        self._count = 0

    def __str__(self):
        """Returns the string of the value"""
        return str(self.value)

    def __repr__(self):
        """Returns the string of the value"""
        return str(self)

    def __eq__(self, other):
        """Defines == between two ScoreTally instances"""
        return self.value == other.value

    def __ne__(self, other):
        """Defines != between two ScoreTally instances"""
        return self.value != other.value

    def __lt__(self, other):
        """Defines < between two ScoreTally instances"""
        return self.value < other.value

    def __le__(self, other):
        """Defines <= between two ScoreTally instances"""
        return self.value <= other.value

    def __gt__(self, other):
        """Defines > between two ScoreTally instances"""
        return self.value > other.value

    def __ge__(self, other):
        """Defines >= between two ScoreTally instances"""
        return self.value >= other.value

    def __add__(self, other):
        """Defines + between two ScoreTally instances"""
        return self.value + other.value

    def __sub__(self, other):
        """Defines - between two ScoreTally instances"""
        return self.value - other.value

    def tally(self, score):
        """Adds a score to the tally and increments the counter"""
        self._score += score
        self._count += 1

    @property
    def value(self):
        """Returns the average of the tallied scores"""
        if self._count > 0:
            return self._score / self._count
        else:
            return 0


class ReinforcementLearner:

    def __init__(self):
        """Initializes the reinforcement learner"""
        self.game = BlackjackGameRunner()
        self._outcomes = {}

    def run_explorer(self, n=1000):
        """Runs the exploration responder

        Args:
            n: Number of iterations to run, default 1000
        """
        self.game.run(self.explorer, n=n)

    def init_prevstate(self, statestr):
        """Adds a new state key to the outcomes dict"""
        self._outcomes[statestr] = {
            'hit': ScoreTally(),
            'stand': ScoreTally()
        }

    @property
    def outcomes(self):
        """Readonly access to the outcomes dict"""
        return self._outcomes

    def explorer(self, state):
        """Responder function that randomly chooses hit or stand
        Also tracks the score in self.outcomes

        Args:
            state: A state dict from a BlackjackGame instance
        """
        prevstate = state['prevstate']
        if state['active']:
            if prevstate is not None:
                if prevstate[0] not in self.outcomes:
                    self.init_prevstate(prevstate[0])
                self.outcomes[prevstate[0]][prevstate[1]].tally(0.1)

            if random.randint(0, 1):
                return 'hit'
            else:
                return 'stand'
        else:
            if prevstate[0] not in self.outcomes:
                self.init_prevstate(prevstate[0])

            score = 0
            if state['outcome'] == 'Win':
                score = 1
            elif state['outcome'] == 'Loss':
                score = -1
            else:
                score = 0
            self.outcomes[prevstate[0]][prevstate[1]].tally(score)

            return None

    def ordered_keys(self):
        """Prints out all potential keys, in order
        The order goes in priority of hard/soft first, then player total
        followed by dealer upcard. Note that if an explorer is run for a low
        number of hands (like 1,000) some keys may never arise.
        """
        for char in ['H', 'S']:
            for x in range(4, 22):
                for y in range(2, 12):
                    key = f"{char}{x}-{y}"
                    yield key

    def action_for_key(self, key):
        """Returns a string with the action having the highest average score"""
        if not key in self.outcomes:
            return None

        actions = self.outcomes[key]
        if actions['hit'] > actions['stand']:
            return 'hit'
        else:
            return 'stand'

    def action_with_diff(self, key):
        """Returns a string with the best action and difference in score
        ie: How much higher is the score for the best action
        """
        if not key in self.outcomes:
            return None

        actions = self.outcomes[key]
        if actions['hit'] > actions['stand']:
            diff = actions['hit'] - actions['stand']
            return f"Hit +{diff}"
        else:
            diff = actions['stand'] - actions['hit']
            return f"Stand +{diff}"
