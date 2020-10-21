#! /usr/local/bin/python3
"""Find the keys to decipher a ciphertext"""

import string
import sys
from random import randint, choice

KNUMRUNS = 15000
KTOTALRUNS = 250000
KSWAPSPACE = 1  # Increase after certain number
KKEEP = 10
KALPHAWEIGHT = 0

"""
The search space is 36!, so we're going to do a greedy algorithm to find
a reasonable sub search space. First we're going to do 1:1 frequency, then
like a genetic algorithm, we'll make a random 2-swap, if we get closer, we
will build upon it, if not we start anew. We will keep all substitutions
that are within a reasonable distance to english text.
"""

def heuristic(english_word_rate, alphabet_rate):
    """
    I was trying to solve others
    and realized I perhaps need to add some
    better search function
    for now it is a simple heuristic
    """
    return english_word_rate + KALPHAWEIGHT*alphabet_rate

def two_swap(frequency):
    """
    Swap two elements randomly
    """
    index = randint(0, len(frequency) - 1)
    next_index = max(0, index + randint(0, KSWAPSPACE)) % (len(frequency))
    frequency[index], frequency[next_index] = frequency[next_index], frequency[index]

def substitute(word, original_frequency, change_frequency):
    """
    Check if a word comes out when tried against a key
    """
    return "".join([original_frequency[change_frequency.index(letter)] for letter in word])

def print_sub(hit_rate, alphabet_rate, frequency, frequency_cipher_text):
    """
    Print to user
    """
    print("The substitution below has a {}% English word rate\
            and a {}% alphabet rate".format(hit_rate*100, alphabet_rate*100))
    print("|" + "|".join(frequency))
    print("|" + "|".join(frequency_cipher_text))

def try_sub(words_in, frequency, frequency_cipher_text, tenkwords):
    """
    Get a hitrate for a key
    """
    count = 0
    alphabetic = 0
    for word in words_in:
        # print("word: " + word)
        new_word = substitute(word, frequency, frequency_cipher_text)
        # print(new_word)
        if all([not letter in "0123456789" for letter in new_word]):
            alphabetic += 1
        if new_word in tenkwords:
            count += 1
    hit_rate = count/len(words_in)
    return (hit_rate, alphabetic/len(words_in))

def main():
    """
    Main program
    Try keys
    """
    alphabet = list(string.ascii_lowercase + string.digits)
    tenkwords = set(open("10kwords.txt").read().splitlines())

    # english frequency in order
    frequency = list("etaoinsrhdlucmfywgpbvkxqjz1234567890")

    if len(sys.argv) < 2:
        print("Please enter a filename after, ./decipher.py filename.txt")
        sys.exit(SystemExit(1))

    filename = sys.argv[1]
    print(filename)
    words_in = open(filename).read().split()
    letters = [letter for word in words_in for letter in word]

    # Get frequency of cipherText
    frequency_of_cipher_text = {}
    for letter in alphabet:
        frequency_of_cipher_text[letter] = 0
    for letter in letters:
        frequency_of_cipher_text[letter] += 1

    # Make first matching
    frequency_cipher_text = ""
    while len(frequency_of_cipher_text) > 0:
        (key, _value) = max(frequency_of_cipher_text.items(), key = lambda k : k[1])
        frequency_cipher_text += key
        del frequency_of_cipher_text[key]
    frequency_cipher_text = list(frequency_cipher_text)

    print(frequency)
    print(frequency_cipher_text)
    best_lists = []
    k = 0
    i = 0
    best_rate = -1
    #ignore global statement for pylint single line
    global KSWAPSPACE  #pylint: disable=global-statement
    while k < KTOTALRUNS:
        if i == KNUMRUNS:
            print("Increasing swap space")
            if KSWAPSPACE >= len(alphabet)-3:
                print("We've exhausted all reasonable swap distances, try changing heuristics")
                break
            i = 0
            KSWAPSPACE += 1
        (hit_rate, alphabetic) = try_sub\
                (words_in, frequency, frequency_cipher_text, tenkwords)
        new_addition = (hit_rate, "".join(frequency_cipher_text), k, alphabetic)
        best_lists.append(new_addition)
        best_lists = sorted(best_lists, key=lambda x: heuristic(x[0], x[3]), reverse=True)[:KKEEP]
        rate = heuristic(hit_rate, alphabetic)
        if rate > best_rate:
            i = 0
            k = 0
            best_rate = rate
            print_sub(hit_rate, rate, frequency, frequency_cipher_text)
        (_, new_frequency_cipher_text, _, _alphabetic_rate) = choice(best_lists)
        frequency_cipher_text = list(new_frequency_cipher_text)
        two_swap(frequency_cipher_text)
        k += 1
        i += 1
    for i in range(KKEEP):
        filey = open("key" + str(i) + ".txt", "w+")
        filey.write("".join(best_lists[i][1]))
        filey.close()

if __name__ == "__main__":
    main()
