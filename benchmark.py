from time import time

from wordle import Wordle
from bot import WordleBot


time_start = time()
performance = {}
for i in range(100):
    print(i)
    wordle = Wordle()
    start_guesses_left = wordle.guesses_left
    wordle_bot = WordleBot()
    wordle_bot.solve(wordle)

    score = start_guesses_left - wordle.guesses_left
    if score not in performance:
        performance[score] = 0
    performance[score] += 1

print(performance)
time_took = time() - time_start

for i in range(20):
    if i > 6:
        print('\033[43m', end='')

    score = performance.get(i, 0)
    print(str(i).rjust(4, ' ') + '|' + '#' * score)

print('\033[0m', end='')
print('time took:', time_took, 'seconds')
