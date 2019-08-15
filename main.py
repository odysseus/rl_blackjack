from deck import *
from blackjackgame import *
from blackjackgamerunner import *
from reinforcementlearner import *

if __name__ == "__main__":
    explorer = ReinforcementLearner()
    explorer.run_explorer(n=10000)

    for key in explorer.ordered_keys():
        if key in explorer.outcomes:
            print(f"{key}: {explorer.action_with_diff(key)}")
