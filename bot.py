from itertools import product

from wordle import Wordle, LetterState, WordleFullException, ANSI_RESET, load_word_list
import logger

logger = logger.Logger(True,
                       False,
                       "$color[$info]$reset $timecolor[%H:%M:%S.%f]$reset $message $tracecolor($filename/$funcname:$line)$reset")
logger.reset_log()

FIRST = 'trace'


class WordleBot:
    def __init__(self):
        self.valid_guess_words = load_word_list('valid-wordle-list.txt')
        self.over_words = load_word_list('todays-wordle-candidate.txt')

    def solve(self, wordle: Wordle):

        print(list(product([LetterState.NONE, LetterState.INCLUDE, LetterState.CORRECT], repeat=5)))

        # valid_words = self.valid_words
        over_words = self.over_words
        valid_guess_words = self.valid_guess_words

        guesses = [(FIRST, wordle.guess(FIRST))]

        logger.log(f'First guess "{FIRST}" done')

        try:
            while 1:

                if guesses[-1][0] in over_words: # remove guessed word from it's possible answer
                    over_words.remove(guesses[-1][0])
                    valid_guess_words.remove(guesses[-1][0])

                over_words = self.possible_words(over_words, guesses[-1]) # filter possible answer by checking the pattern of the earlier guess

                logger.log(f'{len(over_words)} remaining:', over_words)

                print()

                if len(over_words) <= 2:
                    wordle.guess(over_words[0])

                _best = self.best_word(over_words, valid_guess_words)

                # print(_best)
                guesses.append((_best, wordle.guess(_best)))

        except WordleFullException:
            pass

    def count_letters(self, letter: str, word, state: list[LetterState]) -> int:

        count = 0

        for i in range(5):
            if word[i] == letter and (state[i] == LetterState.CORRECT or state[i] == LetterState.INCLUDE):
                count += 1

        return count

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

                if self.count_letters(word[i], guess, state) > self.count_letters(word[i], word, [LetterState.CORRECT] * 5):
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

            for new_state in list(product([LetterState.NONE, LetterState.INCLUDE, LetterState.CORRECT], repeat=5)):

                r = self.possible_words(over_words, (word, new_state))

                if not r: # if the state is impossible
                    continue

                idx = len(r)

                if idx not in _set:
                    _set[idx] = 0

                _set[idx] += 1

            if _set == {}: # if the set is impossible (?)
                continue

            _set = dict(sorted(_set.items()))

            if best_rate is None or best is None:
                logger.error("Assigning", word, _set, "because best doesnt exist")

            if best_rate is None or best is None or self.better2(_set, best_rate):
                best_rate = _set
                best = word
                print(best, best_rate)

        logger.log("best is", best_rate, best)
        return best



    def better2(self, a: dict, b: dict):
        if max(a.keys()) <= max(b.keys()):
            if max(a.keys()) < max(b.keys()):
                return True
            else:
                return sum(a.values()) > sum(b.values())

        return False




if __name__ == '__main__':
    # fuzzy

    wordle = Wordle("deter")

    bot = WordleBot()
    bot.solve(wordle)
    # bot.helps_words(wordle._correct, bot.guess_words)

