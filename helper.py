from wordle import LetterState

def count_letters(letter: str, word, state: list[LetterState]) -> int:
    count = 0

    for i in range(5):
        if word[i] == letter and (state[i] == LetterState.CORRECT or state[i] == LetterState.INCLUDE):
            count += 1

    return count


def possible_words(possible: list[str], _guess: tuple[str, list[LetterState]]) -> list[str]:

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

            if count_letters(word[i], guess, state) > count_letters(word[i], word, [LetterState.CORRECT] * 5):
                break

        else:
            out.append(word)

    return out