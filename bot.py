import typing
from itertools import product

from wordle import Wordle, LetterState, WordleFullException, ANSI_RESET, load_word_list
import reverse
import logger

logger = logger.Logger(True,
                       False,
                       "$color[$info]$reset $timecolor[%H:%M:%S.%f]$reset $message $tracecolor($filename/$funcname:$line)$reset")
logger.reset_log()

FIRST = 'trace'


class WordleBot:
    def __init__(self):
        self.valid_words = load_word_list('valid-wordle-list.txt')
        self.over_words = load_word_list('todays-wordle-candidate.txt')

    def solve(self, wordle: Wordle):

        print(list(product([LetterState.NONE, LetterState.INCLUDE, LetterState.CORRECT], repeat=5)))

        # valid_words = self.valid_words
        over_words = self.over_words

        guesses = [(FIRST, wordle.guess(FIRST))]

        logger.log(f'First guess "{FIRST}" done')

        try:
            while 1:

                if guesses[-1][0] in over_words: # remove guessed word from it's possible answer
                    over_words.remove(guesses[-1][0])

                over_words = self.possible_words(over_words, guesses[-1]) # filter possible answer by checking the pattern of the earlier guess

                logger.log(f'{len(over_words)} remaining:', over_words)

                print()

                if len(over_words) == 1:
                    wordle.guess(over_words[0])
                    assert False

                _best = self.best_word(over_words, load_word_list('valid-wordle-list.txt'))

                # print(_best)
                guesses.append((_best, wordle.guess(_best)))

        except WordleFullException:
            pass

    def possible_words(self, possible: list[str], _guess: tuple[str, list[LetterState]]) -> list[str]:

        out = []

        for word in possible:

            guess, state = _guess

            for i in range(5):

                letter = word[i]
                s = state[guess.find(letter)]

                if letter in guess and s == LetterState.NONE:
                    break

                if state[i] == LetterState.INCLUDE and letter == guess[i]:
                    break

                if state[i] == LetterState.INCLUDE and guess[i] not in word:
                    break

                if state[i] == LetterState.CORRECT and guess[i] is not letter:
                    break

            else:
                out.append(word)

        return out

    def best_word(self, over_words: list[str], guess_words: list[str]) -> str:

        best = None
        best_rate = None

        # for new_state in list(product([LetterState.NONE, LetterState.INCLUDE, LetterState.CORRECT], repeat=5)):
        #     for s in new_state:
        #         print(s + ' ', end=ANSI_RESET)
        #     print()
        # return

        for j, word in enumerate(guess_words):

            # print('\r', j, len(guess_words), end='')

            _set = {}

            # print(word)

            if word == "nails":
                print("!!")

            for new_state in list(product([LetterState.NONE, LetterState.INCLUDE, LetterState.CORRECT], repeat=5)):

                # r = reverse.possible_words(over_words, new_state, word)
                r = self.possible_words(over_words, (word, new_state))

                if not r:
                    continue

                idx = len(r)
                if idx not in _set:
                    _set[idx] = 0
                _set[idx] += 1
            if _set == {}:
                continue
            # print("set", _set)

            if word == "nails":
                print(_set)

            if best_rate is None or best is None:
                logger.error("Assigning", word, _set, "because best doesnt exist")

            if best_rate is None or best is None or self.better2(_set, best_rate):
                best_rate = _set
                best = word
                print(best, best_rate)

        logger.log("best is", best_rate, best)
        return best

    def _rate(self, _set: dict) -> typing.Optional[int]:
        if not _set:
            return None

        # zo groot mogelijk aantal groepen
        # de grootste groep moet zo klein mogelijk zijn

        # return max(_set) - min(_set)
        return max(_set) ** 2 + len(_set)

    def better(self, a: dict, b: dict):  # a > b
        # return len(a.values()) > len(b.values())

        maxa = max(a.values())
        suma = sum(a.values())

        maxb = max(b.values())
        sumb = sum(b.values())

        if suma > sumb:
            return True
        elif suma == sumb:
            return maxa < maxb
        else:
            return False

    def better2(self, a: dict, b: dict):
        return max(a.keys()) < max(b.keys())



if __name__ == '__main__':
    # fuzzy

    wordle = Wordle("paint")

    bot = WordleBot()
    bot.solve(wordle)
    # bot.helps_words(wordle._correct, bot.guess_words)

