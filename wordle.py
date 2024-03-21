from __future__ import annotations

import enum
import random


class WordleInvalidWordException(Exception):
    pass


class WordleFullException(Exception):
    pass


def _load_word_list(filename: str) -> list[str]:
    out = []
    with open(filename, 'r', encoding='utf-8') as file:
        raw = file.read()
    for line in raw.split('\n'):
        if line:
            out.append(line)
    return out


ANSI_RESET = '\033[0m'


class LetterState(enum.StrEnum):
    NONE = '\033[100m'
    INCLUDE = '\033[43m'
    CORRECT = '\033[42m'


class Wordle:
    def __init__(self, correct: None | str = None):
        self._valid_guesses = set(_load_word_list('valid-wordle-list.txt'))
        self.guesses_left = 20  # 6

        if correct is None:
            self._correct = random.choice(_load_word_list('todays-wordle-candidate.txt'))
        else:
            self._correct = correct

        print('wordle correct answer:', self._correct)
        # self._correct = 'boris'

    def guess(self, guess: str) -> list[LetterState]:

        if self.guesses_left <= 0:
            raise WordleFullException()

        if len(guess) != 5 or guess not in self._valid_guesses:
            raise WordleInvalidWordException(f"Invalid guess: {guess}")

        out = self._rate_guess(guess)

        self.guesses_left -= 1

        for i, l in enumerate(out):
            print(l + guess[i] + ANSI_RESET, end='')
        print()

        for l in out:
            if l != LetterState.CORRECT:
                break
        else:
            raise WordleFullException()

        return out

    def _rate_guess(self, guess: str) -> list[LetterState]:

        if len(guess) != 5:
            raise WordleInvalidWordException('Guess length should always be 5')

        out = []

        for i in range(5):
            if self._correct[i] == guess[i].lower():
                out.append(LetterState.CORRECT)
            elif guess[i].lower() in self._correct:
                out.append(LetterState.INCLUDE)
            else:
                out.append(LetterState.NONE)

        return out


if __name__ == '__main__':
    print(LetterState.INCLUDE + 'B' + ANSI_RESET, end='')
    print(LetterState.CORRECT + 'O' + ANSI_RESET, end='')
    print(LetterState.NONE + 'R' + ANSI_RESET, end='')
    print(LetterState.INCLUDE + 'I' + ANSI_RESET, end='')
    print(LetterState.NONE + 'S' + ANSI_RESET, end='')
    print('\n')

    wordle = Wordle(correct=None)
    # wordle.guess('adieu')
    # wordle.guess('story')
    # wordle.guess('iiiii')
    # wordle.guess('boris')

    try:
        while True:
            try:
                wordle.guess(input("Guess a word: "))
            except WordleInvalidWordException:
                print('Invalid word!')
    except WordleFullException:
        print('The answer was: ' + wordle._correct)
