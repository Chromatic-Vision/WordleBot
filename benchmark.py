from time import time

from wordle import Wordle
from bot import WordleBot

SCORE_MAX = 20

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

median = 0
total_frequency = 0
for i in range(SCORE_MAX):
    score = performance.get(i, 0)
    total_frequency += score
frequency = 0
for i in range(SCORE_MAX):
    score = performance.get(i, 0)
    frequency += score
    if frequency > total_frequency // 2:
        median = i
        break
print('median:', median)

for i in range(SCORE_MAX):
    if i > 6:
        print('\033[43m', end='')
    if i == median:
        print('\033[92m', end='')

    score = performance.get(i, 0)
    print(str(i).rjust(4, ' ') + '|' + '#' * score)

    print('\033[0m', end='')

print('\033[0m', end='')
print('time took:', time_took, 'seconds')
