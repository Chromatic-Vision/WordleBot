from __future__ import annotations

import enum
import random


class WordleInvalidWordException(Exception):
    pass


class WordleFullException(Exception):
    pass



def load_word_list(filename: str) -> list[str]:

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

        self._valid_guesses = set(load_word_list('valid-wordle-list.txt'))
        self.guesses_left = 20  # 6
        self.guesses = []

        if correct is None:
            self._correct = random.choice(load_word_list('todays-wordle-candidate.txt'))
        else:
            self._correct = correct

        print('wordle correct answer:', self._correct)


    def guess(self, guess: str) -> list[LetterState]:

        if self.guesses_left <= 0:
            raise WordleFullException()

        if len(guess) != 5 or guess not in self._valid_guesses:
            raise WordleInvalidWordException(f"Invalid guess: {guess}")

        if guess in self.guesses:
            raise WordleInvalidWordException(f"Word {guess} has already been guessed in guess {self.guesses.index(guess) + 1}!")

        try:

            self.guesses.append(guess)
            out = self._rate_guess(guess)

            self.guesses_left -= 1

            for i, l in enumerate(out):
                print(l + guess[i] + ANSI_RESET, end='')

            print()

        except WordleFullException:

            for c in self._correct:
                print(LetterState.CORRECT + c + ANSI_RESET, end='')

            print()
            raise

        return out

    def _rate_guess(self, guess: str) -> list[LetterState]:

        if len(guess) != 5:
            raise WordleInvalidWordException('Guess length should always be 5')

        out = [LetterState.NONE] * 5
        included_letters = {letter: self._correct.count(letter) for letter in set(self._correct)}

        # correct
        for i in range(5):

            if self._correct[i] == guess[i].lower():

                out[i] = LetterState.CORRECT

                included_letters[guess[i].lower()] -= 1

        # include
        for i in range(5):

            if (guess[i].lower() in self._correct) and (guess[i].lower() != self._correct[i].lower()):

                if included_letters[guess[i].lower()] > 0:
                    out[i] = LetterState.INCLUDE
                    included_letters[guess[i].lower()] -= 1

        if guess.lower() == self._correct:
            print(f"You've cleared the wordle with {self.guesses_left} guesses remaining!")
            raise WordleFullException()

        return out


if __name__ == '__main__':

    # print(LetterState.INCLUDE + 'B' + ANSI_RESET, end='')
    # print(LetterState.CORRECT + 'O' + ANSI_RESET, end='')
    # print(LetterState.NONE + 'R' + ANSI_RESET, end='')
    # print(LetterState.INCLUDE + 'I' + ANSI_RESET, end='')
    # print(LetterState.NONE + 'S' + ANSI_RESET, end='')
    # print('\n')

    wordle = Wordle(correct=None)

    try:
        while True:
            try:
                wordle.guess(input("Guess a word: "))
            except WordleInvalidWordException:
                print('Invalid word!')
    except WordleFullException:
        print('The answer was: ' + wordle._correct)
