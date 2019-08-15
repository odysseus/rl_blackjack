from deck import *
from blackjackgame import *
from blackjackgamerunner import *
from reinforcementlearner import *

import unittest
import sys


class TestCard(unittest.TestCase):

    def test_invalid_card(self):
        """Invalid card names should raise an error"""
        with self.assertRaises(InvalidValueError):
            card = Card("Six", "Diamonds")

        with self.assertRaises(InvalidSuitError):
            card = Card("Ace", "Octogons")

    def test_valid_card(self):
        """Valid card names should create successfully"""
        card = Card("6", "Clubs")
        self.assertEqual(str(card), "6 of Clubs")
        self.assertEqual(repr(card), "6 of Clubs")

        card = Card(10, "Spades")
        self.assertEqual(str(card), "10 of Spades")

    def test_card_value(self):
        """Card values should go by Blackjack standards"""
        card = Card('7', 'Diamonds')
        self.assertEqual(card.value, 7)

        card = Card('Queen', 'Hearts')
        self.assertEqual(card.value, 10)

        card = Card('Ace', 'Clubs')
        self.assertEqual(card.value, 1)


class TestDeck(unittest.TestCase):

    def test_deck_creation(self):
        deck = Deck()
        self.assertEqual(len(deck), 52)

    def test_iter(self):
        deck = Deck()
        count = 0
        for card in deck:
            count += 1
            fin = card

        self.assertEqual(str(fin), 'King of Spades')
        self.assertEqual(count, 52)

    def test_draw(self):
        deck = Deck()
        draw = deck.draw(5)
        self.assertEqual(len(draw), 5)
        self.assertEqual(len(deck), 47)

        with self.assertRaises(EmptyDeckError):
            draw = deck.draw(48)

    def test_shuffle(self):
        deck = Deck()
        deck.shuffle()
        for i in range(len(deck.cards)):
            for j in range(len(deck.cards)):
                if i != j:
                    self.assertIsNot(
                        deck.cards[i],
                        deck.cards[j])


class TestHand(unittest.TestCase):

    def test_creation(self):
        hand = Hand()
        self.assertEqual(len(hand), 0)

        hand = Hand([Card(10, 'Spades'), Card(6, 'Clubs')])
        self.assertEqual(len(hand), 2)

    def test_str(self):
        hand = Hand([Card(10, 'Spades'), Card(6, 'Clubs')])
        self.assertEqual(str(hand), '[10 of Spades, 6 of Clubs]')
        self.assertEqual(repr(hand), '[10 of Spades, 6 of Clubs]')

    def test_iter(self):
        hand = Hand([
            Card(6, 'Diamonds'),
            Card('Ace', 'Clubs'),
            Card('Jack', 'Hearts')
        ])

        count = 0
        for card in hand:
            count += 1
            fin = card

        self.assertEqual(count, 3)
        self.assertEqual(str(fin), 'Jack of Hearts')

    def test_add(self):
        hand = Hand([Card('3', 'Clubs'),
                     Card('3', 'Diamonds')])
        hand2 = Hand([Card('4', 'Clubs'),
                      Card('4', 'Spades')])
        cards = [Card('3', 'Spades'),
                 Card('3', 'Hearts')]

        hand + cards
        self.assertEqual(len(hand), 4)
        self.assertEqual(hand.total, 12)

        hand + hand2
        self.assertEqual(len(hand), 6)
        self.assertEqual(hand.total, 20)

        hand + Card('Ace', 'Spades')
        self.assertEqual(len(hand), 7)
        self.assertEqual(hand.total, 21)

        with self.assertRaises(TypeError):
            hand + "dog"

    def test_contains_ace(self):
        ace_first = Hand([Card('Ace', 'Clubs'),
                          Card('Jack', 'Diamonds')])
        ace_last = Hand([Card('Jack', 'Clubs'),
                         Card('Ace', 'Diamonds')])
        no_ace = Hand([Card('King', 'Clubs'),
                       Card('Jack', 'Diamonds')])

        self.assertEqual(ace_first.contains_ace, True)
        self.assertEqual(ace_last.contains_ace, True)
        self.assertEqual(no_ace.contains_ace, False)

    def test_total(self):
        hand = Hand([Card('7', 'Clubs'),
                     Card(6, 'Diamonds')])
        self.assertEqual(hand.total, 13)

        hand = Hand([Card('Jack', 'Clubs'),
                     Card('King', 'Diamonds')])
        self.assertEqual(hand.total, 20)

        hand = Hand([Card('Ace', 'Clubs'),
                     Card(6, 'Diamonds')])
        self.assertEqual(hand.total, 17)

        hand = Hand([Card('Ace', 'Clubs'),
                     Card('King', 'Diamonds')])
        self.assertEqual(hand.total, 21)

        hand = Hand([Card('Ace', 'Clubs'),
                     Card('Ace', 'Diamonds')])
        self.assertEqual(hand.total, 12)

        hand = Hand([Card('Ace', 'Clubs'),
                     Card('Ace', 'Diamonds'),
                     Card('Jack', 'Spades'),
                     Card('9', 'Hearts')])
        self.assertEqual(hand.total, 21)

        hand = Hand([Card('Ace', 'Clubs'),
                     Card('Ace', 'Diamonds'),
                     Card('Ace', 'Spades'),
                     Card('Ace', 'Hearts')])
        self.assertEqual(hand.total, 14)

        hand = Hand([Card('Ace', 'Clubs'),
                     Card('Ace', 'Diamonds'),
                     Card('Ace', 'Spades'),
                     Card('Ace', 'Hearts'),
                     Card('10', 'Spades')])
        self.assertEqual(hand.total, 14)


class TestBlackjackGame(unittest.TestCase):

    def test_init(self):
        game = BlackjackGame()

        self.assertEqual(len(game._deck), 52)
        self.assertEqual(len(game.player), 0)
        self.assertEqual(len(game._dealer), 0)

    def test_deal(self):
        game = BlackjackGame()
        game.deal()

        self.assertEqual(len(game.player), 2)
        self.assertEqual(len(game.dealer), 2)

        # test drawing on an empty deck
        _ = game._deck.draw(46)
        game.deal()
        self.assertEqual(len(game.player), 2)
        self.assertEqual(len(game.dealer), 2)

    def test_upcard_and_total(self):
        game = BlackjackGame()

        game._dealer = Hand([Card('Ace', 'Spades'),
                             Card('6', 'Clubs')])
        game._player = Hand([Card('Jack', 'Clubs'),
                             Card('King', 'Diamonds')])

        self.assertEqual(game.dealer_total, 17)
        self.assertEqual(game.dealer_upcard, 11)
        self.assertEqual(game.player_total, 20)

        game._dealer = Hand([Card('7', 'Spades'),
                             Card('6', 'Clubs')])
        self.assertEqual(game.dealer_upcard, 7)

    def test_bust(self):
        game = BlackjackGame()

        game._dealer = Hand([Card('Ace', 'Spades'),
                             Card('6', 'Clubs')])
        game._player = Hand([Card('Jack', 'Clubs'),
                             Card('King', 'Diamonds')])

        self.assertEqual(game.dealer_bust, False)
        self.assertEqual(game.player_bust, False)

        game._dealer = Hand([Card('Ace', 'Spades'),
                             Card('6', 'Clubs'),
                             Card('10', 'Hearts'),
                             Card('Jack', 'Diamonds')])
        game._player = Hand([Card('Jack', 'Clubs'),
                             Card('King', 'Diamonds'),
                             Card('Ace', 'Clubs'),
                             Card('Ace', 'Hearts')])

        self.assertEqual(game.player_bust, True)
        self.assertEqual(game.dealer_bust, True)

    def test_player_stand(self):
        game = BlackjackGame()
        game.deal()
        self.assertEqual(game.player_standing, False)

        game.player_stand()
        self.assertEqual(game.player_standing, True)

    def test_new_hand(self):
        game = BlackjackGame()
        game._deck = Deck()

        game.deal()
        p_total, d_total = game.player_total, game.dealer_total
        game.deal()

        self.assertNotEqual(p_total, game.player_total)
        self.assertNotEqual(d_total, game.dealer_total)
        self.assertLess(game.player_total, 22)
        self.assertLess(game.dealer_total, 22)

    def test_player_hit(self):
        game = BlackjackGame()
        game._deck = Deck()
        game.deal()

        p_total, p_len = game.player_total, len(game.player)
        game.player_hit()

        self.assertGreater(game.player_total, p_total)
        self.assertGreater(len(game.player), p_len)

    def test_dealer_hit(self):
        game = BlackjackGame()
        game._deck = Deck()
        game.deal()

        d_total, d_len = game.dealer_total, len(game.dealer)
        game.dealer_hit()

        self.assertGreater(len(game.dealer), d_len)
        self.assertGreater(game.dealer_total, d_total)

    def test_prevstate_str(self):
        game = BlackjackGame()
        game._deck = Deck()
        game.deal()
        game.deal()
        self.assertIsNone(game.prevstate)

        game.player_hit()
        self.assertIsNotNone(game.prevstate)
        self.assertEqual(('H13-9', 'hit'), game.prevstate)

    def test_state(self):
        game = BlackjackGame()
        game._deck = Deck()
        game.deal()
        state = game.state()

        self.assertTrue(state['active'])
        self.assertEqual(state['player_total'], 20)
        self.assertEqual(state['dealer_upcard'], 10)

        game.player_stand()
        state = game.state()

        self.assertFalse(state['active'])
        self.assertEqual(state['player_total'], 20)
        self.assertEqual(state['dealer_total'], 20)
        self.assertFalse(state['player_bust'])
        self.assertFalse(state['dealer_bust'])
        self.assertEqual(state['outcome'], 'Push')

        game.deal()
        game.player_hit()
        game.player_stand()
        state = game.state()

        self.assertFalse(state['active'])
        self.assertEqual(state['player_total'], 18)
        self.assertEqual(state['dealer_total'], 17)
        self.assertFalse(state['player_bust'])
        self.assertFalse(state['dealer_bust'])
        self.assertEqual(state['outcome'], 'Win')

        game.deal()
        game.player_hit()
        game.player_hit()
        state = game.state()

        self.assertFalse(state['active'])
        self.assertEqual(state['player_total'], 23)
        self.assertEqual(state['dealer_total'], 7)
        self.assertTrue(state['player_bust'])
        self.assertFalse(state['dealer_bust'])
        self.assertEqual(state['outcome'], 'Loss')

        game.deal()
        game.player_stand()
        game.dealer_hit()
        state = game.state()

        self.assertFalse(state['active'])
        self.assertEqual(state['player_total'], 17)
        self.assertEqual(state['dealer_total'], 27)
        self.assertFalse(state['player_bust'])
        self.assertTrue(state['dealer_bust'])
        self.assertEqual(state['outcome'], 'Win')


class TestBlackjackGameRunner(unittest.TestCase):

    @staticmethod
    def simple_strategy(state):
        """Defines a simple responder function to give to a game runner"""
        if state['active']:
            if state['player_total'] < 17:
                return 'hit'
            else:
                return 'stand'
        else:
            return None

    def test_init(self):
        """Runner should initialize"""
        runner = BlackjackGameRunner()
        self.assertIsNotNone(runner.game)

    def test_failed_run(self):
        """Responders that give invalid responses should raise an error"""
        def invalid_response(state):
            return 'steal'

        with self.assertRaises(InvalidActionError):
            runner = BlackjackGameRunner()
            runner.run(invalid_response)

    def test_successful_run(self):
        """Runner should complete 1000 hands without error"""
        runner = BlackjackGameRunner()
        try:
            runner.run(TestBlackjackGameRunner.simple_strategy, 1000)
        except:
            e = sys.exc_info()[0]
            self.fail(f"Game runner failed with exception {e}")

    def test_end(self):
        """Game should end when given the 'end' response"""
        def end_strategy(state):
            if state['active']:
                return 'hit'
            else:
                return 'end'

        runner = BlackjackGameRunner()
        runner.run(end_strategy)

        # The game will loop infinitely if not given 'end'
        # so reaching this point is proof enough that it works.
        self.assertIsNotNone(runner)


class TestScoreTally(unittest.TestCase):

    def test_str(self):
        tally = ScoreTally()
        self.assertEqual(str(tally), '0')
        self.assertEqual(repr(tally), '0')

    def test_tally_value(self):
        t = ScoreTally()
        self.assertEqual(t.value, 0)
        t.tally(5)
        self.assertEqual(t.value, 5)
        t.tally(1)
        self.assertEqual(t.value, 3)

    def test_comparison(self):
        t1, t2, t3 = ScoreTally(), ScoreTally(), ScoreTally()

        t1.tally(1)
        t1.tally(1)

        t2.tally(1)
        t2.tally(1)

        t3.tally(-1)
        t3.tally(-1)

        self.assertEqual(t1, t2)
        self.assertLess(t3, t1)
        self.assertGreater(t2, t3)
        self.assertTrue(t1 <= t2)
        self.assertTrue(t2 >= t1)
        self.assertTrue(t1 != t3)

    def test_math(self):
        t1, t2 = ScoreTally(), ScoreTally()

        t1.tally(5)
        t1.tally(5)

        t2.tally(2)
        t2.tally(2)

        self.assertEqual(t1 + t2, 7.0)
        self.assertEqual(t1 - t2, 3.0)


class TestReinforcementLearner(unittest.TestCase):

    def test_run_explorer(self):
        rl = ReinforcementLearner()
        rl.run_explorer(n=10)
        self.assertIsNotNone(rl)

    def test_init_prevstate(self):
        key = 'H17-10'
        rl = ReinforcementLearner()
        self.assertFalse(key in rl.outcomes)

        rl.init_prevstate(key)
        self.assertTrue(key in rl.outcomes)
        self.assertTrue('hit' in rl.outcomes[key])
        self.assertTrue('stand' in rl.outcomes[key])
        self.assertIsInstance(rl.outcomes[key]['hit'], ScoreTally)
        self.assertIsInstance(rl.outcomes[key]['stand'], ScoreTally)

    def test_runs(self):
        """Runs an explorer RL for 1000 hands
        Also ensures that correct actions are being found with action_for_key
        and action_with_diff, which similarly require a number of runs to
        populate the state dictionary

        There is a small chance the test will fail because a key is absent or
        or the scores haven't normalized to the correct decision. The keys
        have been chosen specifically to minimize this.
        """
        rl = ReinforcementLearner()
        rl.run_explorer(n=10000)

        self.assertIsNotNone(rl)

        standkey = 'H21-6'
        hitkey = 'H7-10'
        nullkey = 'H17-21'

        self.assertIsNotNone(rl.action_for_key(standkey))
        self.assertIsNotNone(rl.action_for_key(hitkey))
        self.assertIsNone(rl.action_for_key(nullkey))

        self.assertEqual(rl.action_for_key(standkey), 'stand')
        self.assertEqual(rl.action_for_key(hitkey), 'hit')

        self.assertIsNotNone(rl.action_with_diff(hitkey))
        self.assertIsNotNone(rl.action_with_diff(standkey))
        self.assertIsNone(rl.action_with_diff(nullkey))

        self.assertEqual(rl.action_with_diff(hitkey)[0:3], 'Hit')
        self.assertEqual(rl.action_with_diff(standkey)[0:5], 'Stand')

    def test_ordered_keys(self):
        """Checks to ensure the first few keys yielded are in order"""
        expected = ['H4-2', 'H4-3', 'H4-4']
        rl = ReinforcementLearner()
        keys = rl.ordered_keys()

        first = next(keys)
        second = next(keys)
        third = next(keys)
        yielded = [first, second, third]

        for i in range(3):
            self.assertEqual(yielded[i], expected[i])


if __name__ == "__main__":
    unittest.main()
