import math
from itertools import product
from typing import Dict, Tuple, List

from wordle import Wordle, LetterState, load_word_list, WordleFullException
import logger

# ======================================================================================================================

logger = logger.Logger(True,
                       True,
                       "$color[$info]$reset $timecolor[%H:%M:%S.%f]$reset $message $tracecolor($filename/$funcname:$line)$reset")
logger.reset_log()

# ======================================================================================================================

class WordleBot:

    def __init__(self):
        self.valid_guesses = load_word_list('valid-wordle-list.txt')
        self.possible_answers = load_word_list('todays-wordle-candidate.txt')
        self.valid_guesses = self.possible_answers

        self.first_guess = 'trace'

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
                    guesses.append((possible_answers[0], game.guess(possible_answers[0])))
                    continue

                _best = self.optimal_word(possible_answers, valid_guesses)[0]

                # print(_best)
                guesses.append((_best, game.guess(_best)))

        except WordleFullException:
            pass

    def optimal_word(self, remaining: list[str], valid_guesses: list[str]) -> list[str]:

        optimal_words = []
        optimal_set = {}
        optimal_bits = 0

        for word in valid_guesses:

            current_set = {}
            current_bits = 0
            possible_matches = 0

            for pattern in list(product([LetterState.NONE, LetterState.INCLUDE, LetterState.CORRECT], repeat=5)):

                possibles = self.helper.possible_words(remaining, (word, pattern))

                if possibles:
                    current_set[pattern] = possibles
                    possible_matches += possibles.__len__()
                    current_bits += ((-math.log2(possibles.__len__() / remaining.__len__())) * (possibles.__len__() / remaining.__len__()))

            # print("\r", word, end="")

            if optimal_set == {}:
                optimal_words = [word]
                optimal_set = current_set
                optimal_bits = current_bits

            else:

                if optimal_bits < current_bits:

                    optimal_words = [word]
                    optimal_set = current_set
                    optimal_bits = current_bits

                    print()
                    print(current_bits, word)
                    print()

                elif optimal_bits == current_bits:
                    match (self.compare_dicts(current_set, optimal_set)):
                        case 1:
                            optimal_words = [word]
                            optimal_set = current_set
                        case 0:
                            optimal_words.append(word)
                        case -1:
                            pass
                else:
                    pass

        print()
        print(f"optimal is {optimal_words}")
        print(f"{optimal_set}")
        return optimal_words

    def compare_dicts(
            self,
            dict1: Dict[Tuple[LetterState, ...], List[str]],
            dict2: Dict[Tuple[LetterState, ...], List[str]]
    ) -> int:
        """
        Compare two dictionaries based on the number of groups (keys) and the size of the largest group.

        Returns:
            - 1 if dict1 is better
            - -1 if dict2 is better
            - 0 if they are equal
        """

        def evaluate_dict(d: Dict[Tuple[LetterState, ...], List[str]]) -> Tuple[int, int]:
            num_groups = len(d)
            max_group_size = max(len(words) for words in d.values())
            return (num_groups, max_group_size)

        num_groups1, max_group_size1 = evaluate_dict(dict1)
        num_groups2, max_group_size2 = evaluate_dict(dict2)

        # Compare based on the number of groups first
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

        assert state.__len__() == 5, state.__len__()

        count = 0

        for i in range(5):
            if word[i] == letter and (state[i] == LetterState.CORRECT or state[i] == LetterState.INCLUDE):
                count += 1

        return count

    def confirmed_letter_count(self,
                                letter: str,
                                word,
                                state: list[LetterState]) -> bool:

        count = 0
        confirmed = False

        for i in range(5):
            if word[i] == letter and (state[i] == LetterState.CORRECT or state[i] == LetterState.INCLUDE):
                count += 1

        if count >= 0:
            for i in range(5):
                if word[i] == letter and (state[i] == LetterState.NONE):
                    confirmed = True

        return confirmed

    def possible_words(self, possible: list[str], _guess: tuple[str, list[LetterState]]) -> list[str]:

        out = []

        for word in possible:

            guess, state = _guess

            for i in range(5):

                letter = word[i]

                if state[i] == LetterState.INCLUDE and letter == guess[i]:
                    break

                if state[i] == LetterState.INCLUDE and guess[i] not in word:
                    break

                if state[i] == LetterState.CORRECT and guess[i] is not letter:
                    break

                if self.count_letters(letter, guess, state) > self.count_letters(letter, word, [LetterState.CORRECT] * 5):
                    break

                # als de guess REFER 2 Rs heeft betekent dat BORIS geen antwoord kan zijn

                if self.confirmed_letter_count(letter, guess, state): # als je TEPEE guesst en er komt maar 2 E's geel en 3e grijs weet je dat er allen maar 2 E's zijn
                    # logger.log("confirmed")
                    if self.count_letters(letter, word, [LetterState.CORRECT] * 5) != self.count_letters(letter, guess, state):
                        # logger.log("impossible", word, guess)
                        break

            else:
                out.append(word)

        return out



if __name__ == "__main__":

    wordle = Wordle("storm")

    bot = WordleBot()
    bot.solve(wordle)
    # print(WordleBot().helper.considered_letter_count("e", "tepee", [LetterState.NONE, LetterState.CORRECT, LetterState.NONE, LetterState.NONE, LetterState.NONE]))