from wordle import Wordle, LetterState, WordleFullException
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


Guess = tuple[str, list[LetterState]]


class WordleBot:
    def __init__(self):
        self.valid_words = _load_word_list('valid-wordle-list.txt')
        self.guess_words = _load_word_list('todays-wordle-candidate.txt')

    def solve(self, wordle: Wordle):
        valid_words = self.valid_words
        guess_words = self.guess_words

        guesses = [(FIRST, wordle.guess(FIRST))]

        logger.log(f'First guess "{FIRST}" done')
        try:
            while True:
                if guesses[-1][0] in guess_words:
                    guess_words.remove(guesses[-1][0])
                if guesses[-1][0] in valid_words:
                    valid_words.remove(guesses[-1][0])
                guess_words = self.possible_words(guess_words, guesses[-1])
                valid_words = self.possible_words(valid_words, guesses[-1])

                if len(guess_words) == 0:
                    wordle.guess(guess_words[-1])
                else:
                    highest_removed_score = None
                    highest_removed = None
                    for word in guess_words:
                        score = self.helps_words(word, guess_words)
                        if highest_removed_score is None or score > highest_removed_score:
                            highest_removed_score = score
                            highest_removed = word
                    # print('best:', highest_removed)
                    if highest_removed is None:
                        raise NotImplementedError
                    guesses.append((highest_removed, wordle.guess(highest_removed)))
                    logger.log('guess_words:', str(len(guess_words)).rjust(5, ' '), guess_words)
        except WordleFullException:
            return

    def possible_words(self, possible: list[str], _guess: Guess) -> list[str]:
        # possible = possible.copy()
        # print('possible words:', possible)
        out = []
        for word in possible:
            guess, state = _guess
            for i in range(5):
                s = state[guess.find(word[i])]
                if word[i] in guess and s == LetterState.NONE:
                    # print('skipped', word)
                    break
                if word[i] == guess[i] and state[i] == LetterState.INCLUDE:
                    break
                if word[i] != guess[i] and state[i] == LetterState.CORRECT:
                    break

            else:
                out.append(word)

        return out

    def helps_words(self, guess: str, words: list[str]) -> int:
        out = 0
        for word in words:
            for letter in guess:
                if letter in word:
                    out += 1
                    break

        return out


if __name__ == '__main__':
    wordle = Wordle()
    bot = WordleBot()
    bot.solve(wordle)

    def _log(v):
        print(v)
        return v

    assert 'expel' not in _log(bot.possible_words(['expel'], ('blimp',
                                                         [LetterState.CORRECT, LetterState.CORRECT,
                                                          LetterState.NONE, LetterState.NONE, LetterState.CORRECT])))
