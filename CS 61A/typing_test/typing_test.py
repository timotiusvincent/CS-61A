""" Typing Test implementation """

from utils import *
from ucb import main

# BEGIN Q1-5
"*** YOUR CODE HERE ***"
def lines_from_file(path):
    texts = list()
    paragraphs = open(path, mode = 'r')
    texts = readlines(paragraphs)
    close(paragraphs)
    i = 0
    while i < len(texts):
         texts[i] = texts[i].strip()
         i += 1
    return texts

def new_sample(path, i):
    texts = lines_from_file(path)
    return texts[i]

def analyze(sample_paragraph, typed_string, start_time, end_time):
    """ Problem number 2. A function that analyze the accuracy and time for the
    typing test.
    """
    analyzed_data = list()
    total_words = len(typed_string) / 5
    total_time = (end_time - start_time) / 60
    words_per_min = total_words / total_time

    i, total_correct, total_words = 0, 0, 0
    original_text = split(sample_paragraph)
    user_text = split(typed_string)
    if len(user_text) > 0:
        while i < min(len(original_text), len(user_text)):
            if original_text[i] == user_text[i]:
                total_correct += 1
            total_words += 1
            i += 1
        accuracy_perc = total_correct / total_words * 100
    else:
        accuracy_perc = 0.0

    analyzed_data.append(words_per_min)
    analyzed_data.append(accuracy_perc)
    return analyzed_data

def pig_latin(text):
    """Question number 3. Generate a giberish text from the provided text.
    Works by adding way or ay and changing the order of the first consonant.
    """
    if (text[0] == 'a' or text[0] == 'i' or text[0] == 'u' or text[0] == 'e'
        or text[0] == 'o'):
        return text + "way"
    i = 0
    appended_text = ""
    while (text[i] != 'a' and text[i] != 'i' and text[i] != 'u' and text[i] != 'e'
        and text[i] != 'o'):
        appended_text += text[i]
        i += 1
        if i >= len(text):
            return text + "ay"
    return text[len(appended_text):] + appended_text + "ay"

def autocorrect(user_input, words_list, score_function):
    """Question number 4. A simple autocorrect function just like the one
    in your phone.
    """
    if user_input in words_list:
        return user_input
    else:
        return min(words_list, key = lambda x: score_function(user_input, x))

def swap_score(word1, word2):
    """ Question number 5. First score_function that uses recursion."""
    if min(len(word1), len(word2)) == 0:
        return 0
    elif word1[0] != word2[0]:
        return 1 + swap_score(word1[1:], word2[1:])
    else:
        return 0 + swap_score(word1[1:], word2[1:])
# END Q1-5

# Question 6

def score_function(word1, word2):
    """A score_function that computes the edit distance between word1 and word2."""

    if word1 == word2[:len(word1)]:     # return the difference between word1 and word2
        return len(word2[len(word1):])

    elif len(word2) == 0 or len(word1) == 0: # Fill in the condition
        # BEGIN Q6
        "*** YOUR CODE HERE ***"
        if len(word1) != 0:
            return len(word1)
        return 0
        # END Q6

    elif word1[0] == word2[0]: # Feel free to remove or add additional cases
        # BEGIN Q6
        "*** YOUR CODE HERE ***"
        if len(word2) == 0:     # end recursive calls at the end of the second word
            return 0
        return 0 + score_function(word1[1:], word2[1:])
        # END Q6

    else:
        add_char = word2[0] + word1[0:]  # Fill in these lines
        remove_char = word1[1:]
        substitute_char = word2[0] + word1[1:]
        # BEGIN Q6
        "*** YOUR CODE HERE ***"
        found = False
        for i in range(min(len(word1), len(word2))):    # Checks if there are characters that
            if word1[i] == word2[i]:                    # falls in the same place for both words
                found = True

        if len(word1) < len(word2) and not found:
            return 1 + score_function(add_char, word2)
        elif len(word1) == 1:
            return 1 + score_function(substitute_char, word2)
        elif len(word1) > len(word2) or word1[1] == word2[0]:
            return 1 + score_function(remove_char, word2)
        return 1 + score_function(substitute_char, word2)
        # END Q6

KEY_DISTANCES = get_key_distances()

# BEGIN Q7-8
"*** YOUR CODE HERE ***"
def score_function_accurate(word1, word2):
    """ Question number 7. Implementing a more accurate score function by using
    the get_key_distances function. Implementation of most lines are similar to
    the previous score function with a slight changes in the return value of
    substituting a character in the string
    """
    if word1 == word2[:len(word1)]:
        return len(word2[len(word1):])

    elif len(word2) == 0 or len(word1) == 0:
        if len(word1) != 0:
            return len(word1)
        return 0

    elif word1[0] == word2[0]:
        if len(word2) == 0:
            return 0
        return 0 + score_function_accurate(word1[1:], word2[1:])

    else:
        add_char = word2[0] + word1[0:]
        remove_char = word1[1:]
        substitute_char = word2[0] + word1[1:]
        distance = KEY_DISTANCES[word1[0], word2[0]]
        found = False

        for i in range(min(len(word1), len(word2))):
            if word1[i] == word2[i]:
                found = True

        if len(word1) < len(word2) and not found:
            return 1 + score_function_accurate(add_char, word2)
        elif len(word1) == 1:
            return distance + score_function_accurate(substitute_char, word2)
        elif len(word1) > len(word2) or word1[1] == word2[0]:
            return 1 + score_function_accurate(remove_char, word2)
        return distance + score_function_accurate(substitute_char, word2)

def score_function_final(word1, word2):
    """ Question number 8. Implementing final score function that uses memoization
    by implementing a dictionary that stores all previous calculation on two sets
    of words
    """
    memo = {}
    find_key1 = word1 + ',' + word2             # key number 1 for dictionary
    find_key2 = word2 + ',' + word1             # key number 2 for dictionary
    if find_key1 not in memo and find_key2 not in memo:
        total_score = score_function_accurate(word1, word2)
        memo[find_key1] = total_score           # create dictionary entry for both keys
        memo[find_key2] = total_score
        return total_score
    return max(memo[find_key1], memo[find_key2])

# END Q7-8
