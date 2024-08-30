import os

from wordle import Wordle, WordleFullException, LetterState


class WordleBot:
    def __init__(self):
        pass

    def solve(self, wordle: Wordle):
        with open('tarse.tree', 'r', encoding='ascii') as tree:
            def state_to_string(state: list[LetterState]) -> str:
                out = ''
                for s in state:
                    if s == LetterState.NONE:
                        out += 'B'
                    elif s == LetterState.INCLUDE:
                        out += 'Y'
                    elif s == LetterState.CORRECT:
                        out += 'G'
                    else:
                        raise AssertionError()
                return out

            try:
                while 1:
                    word = tree.read(6)[:-1]
                    last_state = state_to_string(wordle.guess(word))

                    state = None
                    while state != last_state:
                        line = tree.read(5 + 10 + 1)[:-1]
                        state, index = line[:5], line[5:]
                        index = int(index)

                    tree.seek(index)
            except WordleFullException:
                pass


if __name__ == '__main__':
    wordle = Wordle()

    bot = WordleBot()
    bot.solve(wordle)
