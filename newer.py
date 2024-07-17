import math
from itertools import product
from typing import Dict, Tuple, List

from wordle import Wordle, LetterState, load_word_list, WordleFullException
import logger

# ======================================================================================================================

logger = logger.Logger(True,
                       False,
                       "$color[$info]$reset $timecolor[%H:%M:%S.%f]$reset $message $tracecolor($filename/$funcname:$line)$reset")
logger.reset_log()

# ======================================================================================================================

class WordleBot:

    def __init__(self):
        self.valid_guesses = load_word_list('valid-wordle-list.txt')
        self.possible_answers = load_word_list('todays-wordle-candidate.txt')

        self.first_guess = 'crane'

        self.helper = WordleHelper()

    def solve(self, game: Wordle):

        valid_guesses = self.valid_guesses
        possible_answers = self.possible_answers


        guesses = [(self.first_guess, game.guess(self.first_guess))]

        logger.log(f'First guess "{self.first_guess}" done')

        try:

            while 1:

                if guesses[-1][0] in possible_answers: # remove guessed word from possible answers
                    possible_answers.remove(guesses[-1][0])

                if guesses[-1][0] in valid_guesses: # remove guessed word from valid guesses
                    valid_guesses.remove(guesses[-1][0])

                possible_answers = self.helper.possible_words(possible_answers, guesses[-1]) # filter possible answer by checking the pattern of the earlier guess

                logger.log(f'{len(possible_answers)} possible answers remaining:', possible_answers)

                print()

                if 0 < len(possible_answers) <= 2:
                    game.guess(possible_answers[0])

                    if 0 < len(possible_answers) <= 2:
                        game.guess(possible_answers[0])

                        if 0 < len(possible_answers) <= 2:
                            game.guess(possible_answers[0])

                _best = self.optimal_word(possible_answers, valid_guesses)[0]

                # print(_best)
                guesses.append((_best, game.guess(_best)))

        except WordleFullException:
            pass

    def optimal_word(self, remaining: list[str], valid_guesses: list[str]) -> list[str]:

        optimal_words = []
        optimal_set = {}

        for word in valid_guesses:

            current_set = {}

            for pattern in list(product([LetterState.NONE, LetterState.INCLUDE, LetterState.CORRECT], repeat=5)):

                possibles = self.helper.possible_words(remaining, (word, pattern))

                if possibles:
                    current_set[pattern] = possibles

            print("\r", word, end="")

            if optimal_set == {}:
                optimal_words = [word]
                optimal_set = current_set
            else:
                match (self.compare_dicts(current_set, optimal_set)):
                    case 1:
                        optimal_words = [word]
                        optimal_set = current_set
                    case 0:
                        optimal_words.append(word)
                    case -1:
                        pass

        print()
        print(f"optimal is {optimal_words}")
        print(f"{optimal_set}")
        return optimal_words

    def compare_dicts(
            self,
            a: Dict[Tuple[LetterState, ...], List[str]],
            b: Dict[Tuple[LetterState, ...], List[str]],
            normalization_factor: int = 14855
    ) -> int:
        """
        Compare two dictionaries based on the number of groups (keys) and the size of the largest group.

        Returns:
            - 1 if dict1 is better
            - -1 if dict2 is better
            - 0 if they are equal
        """

        def evaluate_dict(d: Dict[Tuple[LetterState, ...], List[str]]) -> Tuple[float, int, int]:
            num_groups = len(d)
            max_group_size = max(len(words) for words in d.values())
            total_length_of_words = sum(len(words) for words in d.values())
            p = total_length_of_words / normalization_factor
            total_bits = math.log2(1 / p)
            return (total_bits, num_groups, max_group_size)

        total_bits1, num_groups1, max_group_size1 = evaluate_dict(a)
        total_bits2, num_groups2, max_group_size2 = evaluate_dict(b)

        # Compare based on total bits of information first
        if total_bits1 > total_bits2:
            print(total_bits1, total_bits2)
            return 1
        elif total_bits1 < total_bits2:
            return -1
        else:
            # If total bits of information is the same, compare based on the number of groups
            if num_groups1 > num_groups2:
                return 1
            elif num_groups1 < num_groups2:
                return -1
            else:
                # If the number of groups is the same, compare based on the size of the largest group
                if max_group_size1 < max_group_size2:
                    return 1
                elif max_group_size1 > max_group_size2:
                    return -1
                else:
                    return 0



class WordleHelper:

    def __init__(self):
        pass

    def count_letters(self, letter: str, word, state: list[LetterState]) -> int:
        count = 0

        for i in range(5):
            if word[i] == letter and (state[i] == LetterState.CORRECT or state[i] == LetterState.INCLUDE):
                count += 1

        return count

    def possible_words(self, possible: list[str], _guess: tuple[str, list[LetterState]]) -> list[str]:

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

                if self.count_letters(word[i], guess, state) > self.count_letters(word[i], word, [LetterState.CORRECT] * 5):
                    break

            else:
                out.append(word)

        return out



if __name__ == "__main__":

    wordle = Wordle("terse")

    bot = WordleBot()
    bot.solve(wordle)