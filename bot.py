import typing

from wordle import Wordle, LetterState, WordleFullException, ANSI_RESET
import reverse
import logger

logger = logger.Logger(True,
                       False,
                       "$color[$info]$reset $timecolor[%H:%M:%S.%f]$reset $message $tracecolor($filename/$funcname:$line)$reset")
logger.reset_log()

FIRST = 'trace'


def _load_word_list(filename: str) -> list[str]:
    out = []
    with open(filename, 'r', encoding='utf-8') as file:
        raw = file.read()
    for line in raw.split('\n'):
        if line:
            out.append(line)
    return out


class WordleBot:
    def __init__(self):
        self.valid_words = _load_word_list('valid-wordle-list.txt')
        self.guess_words = _load_word_list('todays-wordle-candidate.txt')

    def solve(self, wordle: Wordle):
        # valid_words = self.valid_words
        guess_words = self.guess_words

        guesses = [(FIRST, wordle.guess(FIRST))]

        logger.log(f'First guess "{FIRST}" done')

        try:
            while 1:

                if guesses[-1][0] in guess_words:
                    guess_words.remove(guesses[-1][0])
                # if guesses[-1][0] in valid_words:
                #     valid_words.remove(guesses[-1][0])

                guess_words = self.possible_words(guess_words, guesses[-1])
                # valid_words = self.possible_words(valid_words, guesses[-1])

                logger.log(f'{len(guess_words)} remaining:', guess_words)

                print()

                # highest_removed_score = None
                # highest_removed = None
                #
                # for word in guess_words:
                #     score = len(self.helps_words(word, guess_words))
                #
                #     if highest_removed_score is None or score > highest_removed_score:
                #
                #         highest_removed_score = score
                #         highest_removed = word
                #
                # if highest_removed is None:
                #     raise NotImplementedError

                _best = self.best_word(guess_words)

                # print(_best)
                guesses.append((_best, wordle.guess(_best)))

        except WordleFullException:
            pass

    def possible_words(self, possible: list[str], _guess: tuple[str, list[LetterState]]) -> list[str]:
        # possible = possible.copy()
        # print('possible words:', possible)
        out = []
        for word in possible:
            guess, state = _guess
            for i in range(5):

                letter = word[i]
                s = state[guess.find(letter)]

                if letter in guess and s == LetterState.NONE: # als een letter in een guess zit waarvan dat fout is
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

    def best_word(self, guess_words: list[str]) -> str:

        best = None
        best_rate = None

        for j, word in enumerate(guess_words):
            print(j, len(guess_words))

            _set = {}

            for i in range(3**5):

                new_state = [[LetterState.NONE, LetterState.INCLUDE, LetterState.CORRECT][i // ((j * 3) or 1) % 3] for j in range(5)]
                # print(' '.join(new_state) + ANSI_RESET)

                r = reverse.possible_words(guess_words, new_state, word)

                if not r:
                    continue

                idx = len(r)
                if idx not in _set:
                    _set[idx] = 0
                _set[idx] += 1

            rate = self._rate(_set)
            if rate is None:
                continue
            if best is None or best_rate is None or best_rate < rate:
                best_rate = rate
                best = word

        return best

    def _rate(self, _set: dict) -> typing.Optional[int]:
        if not _set:
            return None

        # zo groot mogelijk aantal groepen
        # de grootste groep moet zo klein mogelijk zijn

        # return max(_set) - min(_set)
        return max(_set) ** 2 + len(_set)


if __name__ == '__main__':
    wordle = Wordle("shank")
    bot = WordleBot()
    bot.solve(wordle)
    # bot.helps_words(wordle._correct, bot.guess_words)