from wordle import load_word_list, LetterState


# ⬛🟨🟩  # black, yellow, green


def possible_words(possible: list[str], state: list[LetterState], correct: str) -> list[str]:
    out = []
    for word in possible:
        for i in range(5):
            if (
                    state[i] == LetterState.CORRECT
                    and word[i] != correct[i]
            ):
                break
            if (
                    state[i] != LetterState.CORRECT
                    and word[i] == correct[i]
            ):
                break
            if (
                    state[i] == LetterState.NONE
                    and word[i] in correct
            ):
                break

        else:
            out.append(word)

    return out


def letter_state_from_emoji(emoji: str) -> LetterState:
    try:
        return {
            '⬛': LetterState.NONE,
            '🟨': LetterState.INCLUDE,
            '🟩': LetterState.CORRECT
        }[emoji]
    except KeyError:
        raise ValueError(f'Unknown emoji "{emoji}"')


class ReverseWordleSolver:
    def __init__(self, correct: str):
        self.valid_words = load_word_list('valid-wordle-list.txt')
        self.guess_words = load_word_list('todays-wordle-candidate.txt')
        self.correct = correct

    def solve(self, line: str) -> tuple[list[str], list[str]]:
        if len(line) != 5:
            raise ValueError('len(line) should be 5 characters')
        state = [letter_state_from_emoji(line[i]) for i in range(5)]

        return (
            possible_words(self.valid_words, state, self.correct),
            possible_words(self.guess_words, state, self.correct)
        )


if __name__ == '__main__':
    solver = ReverseWordleSolver('finch')
    emojis = [
        ('⬛⬛⬛⬛⬛', 'salet'),
        ('⬛⬛🟨🟨⬛', 'plink'),
        ('⬛🟩🟩⬛⬛', 'zinky'),
        ('🟩⬛⬛⬛⬛', 'forgo'),
        ('🟩🟩🟩🟩🟩', 'finch')
    ]
    for emoji in emojis:
        solution, guess_solution = solver.solve(emoji[0])
        print(len(solution), '/', len(solver.valid_words), '\t| ', len(guess_solution), '/', len(solver.guess_words))
        assert emoji[1] in solution
        print(solution)

    test = """⬛⬛⬛🟩⬛
⬛⬛🟨🟨⬛
⬛🟩🟩🟩⬛
⬛🟩🟩🟩🟩
⬛🟩🟩🟩🟩
🟩🟩🟩🟩🟩"""
    for emoji in test.split('\n'):
        print(solver.solve(emoji)[0])