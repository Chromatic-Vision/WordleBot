from wordle import Wordle, LetterState
import logger

logger = logger.Logger(True,
                       False,
                       "$color[$info]$reset $timecolor[%H:%M:%S.%f]$reset $message $tracecolor($filename/$funcname:$line)$reset")
logger.reset_log()

FIRST = 'crane'


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
        valid_words = self.valid_words
        guess_words = self.guess_words

        guesses = [(FIRST, wordle.guess(FIRST))]

        logger.log(f'First guess "{FIRST}" done')

        b = 0

        while wordle.guesses_left > 0:

            if guesses[-1][0] in guess_words:
                guess_words.remove(guesses[-1][0])
            if guesses[-1][0] in valid_words:
                valid_words.remove(guesses[-1][0])

            # print("before", guess_words.__len__())

            guess_words = self.possible_words(guess_words, guesses[-1])
            valid_words = self.possible_words(valid_words, guesses[-1])

            # print("after", guess_words.__len__())

            logger.log(f'{len(guess_words)} remaining:', guess_words)

            print()

            highest_removed_score = None
            highest_removed = None

            for word in guess_words:
                score = len(self.helps_words(word, valid_words))

                if highest_removed_score is None or score > highest_removed_score:

                    highest_removed_score = score
                    highest_removed = word

            b += 1

            # print('best:', highest_removed)
            #
            # logger.log("Guessing", highest_removed)

            if highest_removed is None:
                raise NotImplementedError
            guesses.append((highest_removed, wordle.guess(highest_removed)))

        return b

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

                if letter == guess[i] and state[i] == LetterState.INCLUDE:
                    break

                if state[i] == LetterState.CORRECT and guess[i] is not letter:
                    break

            else:
                out.append(word)

        return out

    def helps_words(self, guess: str, words: list[str]) -> list[str]: # TODO: ??
        out = []
        for word in words:
            for letter in guess:
                if letter in word:
                    out.append(word)
                    break

        return out



if __name__ == '__main__':
    wordle = Wordle()
    bot = WordleBot()
    bot.solve(wordle)
