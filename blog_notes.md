# Things to Write About

## Coding

### Card

- Start with a simple `Card` class and them demonstrate how nonsense cards, such as the "Duke of Octogons" can be created.
- There's a more nefarious error is we accidentally use code like `Card('Six', 'Clubs')`, which looks correct but ends up making the `value` equal to 10 since we treat all 'named' cards (where the name is a string) as being a value of 10 unless it's an 'Ace'
- Explicitly stating which names can be used fixes this. This probably isn't completely necessary since the only time `Card` is used directly is in testing and by the `Deck` class, and it makes the program run a little bit slower. Having said that, more error checking is always better and since we only create 52 cards at a time the runtime effect is minimal. I will trade 'less error prone' for 'runs an imperceptible amount slower'

### Deck

- Ultimately this class is just wrapping/extending a list, and thus our **dunder**  (double underscore) methods are just passing forward the same operations on `self.cards`

### Hand

- As with `Deck` this class largely just forwards functionality from `List`, and adds behavior methods unique to a `Hand`
- Note that we are iteratively building the functionality we need with methods like `contains_ace()`, `total()`, and `bust()`--each of these relies on the ones before it.


### BlackjackGame

- This is all pretty straightforward since we have been including what we need in the other classes in regards to things like busting, hand totals, drawing from the deck, etc. This keeps the logic clean as we aren't trying to calculate the hand total in the `BlackjackGame` class--something that, while possible, seems separate from the logic of the game itself.
- Methods like `dealer_total()` might seem redundant because we could replace `game.dealer_total()` with `game.dealer.total()` and get the same result, but it's bad practice to 'reach through' classes like that. If the `Hand` class changed or was replaced we could just fix `dealer_total()` in that one spot and we wouldn't have to look for other occurrences, but if we used `game.dealer.total()` we might have to fix _every_ occurrence.

## Testing

### Coverage

Using `coverage.py` library, commands are:

```
C:...> coverage run tests.py
C:...> coverage report -m
```

The `-m` option explicitly mentions which lines are missing, at the expense of more verbose output.


### Card

- Mainly we need to ensure that invalid cards get rejected and valid cards don't, which isn't too hard.
- We want to test the special case of something like `Card('Six', 'Diamonds')`, in our case it should get rejected but we don't want cards ending up with improper values (Like 10 when it should be 6).
- Testing errors requires the use of the `with` construct. Classes that implement `with` use special `__enter__` and `__exit__` dunder methods to handle situations that might raise errors. In this case we _want_ errors to be raised so we specify precisely which error we expect (and want) and the class will handle it being raised without crashing the program.
- Card value is more straightforward because we have already prevented any named cards from being created that _aren't_ approved, so really it's just testing the 2-9 values, that named cards are 10, and that Aces are 1.


### Deck

- A lot of these methods just pass through functionality used in lists so we can assume that they have been tested more than we ever will and that they work fine. Having said that for the sake of code coverage we should include some simple tests that at least deal with the method itself. Even a basic test will catch some things that would be missed if we had no test at all.
- For creation we just ensure that a full deck of cards has been created
- For iteration we make sure that the final item iterated over is the last card in an unshuffled deck, and that we go through 52 items.
- For draw we ensure that we can draw cards when it is valid, and get an error when we draw too many.
- For shuffling we just ensure that no two array elements point to the same object


### Hand

- Creation we are just testing the call to `__init__` and getting `__len__` at the same time.
- We test `__str__` and `__repr__` together since we are using the same value for each in this class.
- For `contains_ace()` we want to check for an ace at the beginning and end of the hand, also a hand with none.
- `total()` is the trickiest because there are so many edge cases.

## Design
