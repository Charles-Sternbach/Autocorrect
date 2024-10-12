# -*- coding: utf-8 -*-
"""
Purpose:
Develop a script that will autocorrect an input file with suggestions for
corrections. Uses numerous methods to generate potential candidate corrections.

@author: Charles Sternbach
"""

def get_files():
    """Prompts the user to enter file names and returns them.

    Ask the user to provide the names of three files: A dictionary file,
    an input file, and a keyboard file. The inputs are displayed back
    to the user.

    Returns:
        tuple: A tuple containing three strings: A dictionary file,
            an input file, and a keyboard file in that order.
    """
    dictionary_file = input('Dictionary file => ')
    print(dictionary_file)
    input_file = input('Input file => ')
    print(input_file)
    keyboard_file = input('Keyboard file => ')
    print(keyboard_file)

    return dictionary_file, input_file, keyboard_file


def correct_word(word):
    pass


def get_dictionary(dictionary_file):
    """Read provided dictionary file into a python dictionary.

    Args:
        dictionary_file: A text file containing words and their corresponding
            frequencies in the lexicon delimited by a comma (,).

    Returns:
        dict: A dict mapping words in the provided dictionary to their
        corresponding frequency in the lexicon.
    """
    f2 = open(dictionary_file, 'r')
    english_dictionary = dict()
    lines = f2.readlines()  # copies from a file in file system and stores into python list.
    for line in lines:
        k, v = line.split(',')
        v = v.replace('\n', '')
        english_dictionary[k] = v
    f2.close()
    return english_dictionary


def auto_correct_file(dictionary, input_file, keyboard_dictionary):
    """Autocorrect words from the input file.

    Attempts to autocorrect each word by dropping, or inserting a letter.
    Swapping two consecutive letters in the word.
    Replacing a single letter in the word with any other letter from the
        possible replacements in the keyboard file.
    If a replacement is found, display up to three possible replacements
        for the word.

    Args:
        dictionary: Python dictionary containing words and their corresponding
            frequencies in the lexicon delimited by a comma (,).
        input_file: A text file containing words to be corrected.
        keyboard_dictionary: Python dictionary mapping letters
            to the surrounding keys that are around each letter on the keyboard.
    """
    keys_correctly_spelled_words = dictionary.keys()
    f3 = open(input_file, 'r')
    words = f3.readlines()

    for word in words:
        word = word.strip()
        if word in keys_correctly_spelled_words:
            print("%s -> FOUND" % (justify_right(word, 15)))  # Done - Its already spelled correctly
        else:  # Lines below will auto-correct the word.
            drop_list    = create_drop_list(word, keys_correctly_spelled_words)
            insert_list  = create_insert_list(word, keys_correctly_spelled_words)
            swap_list    = create_swap_list(word, keys_correctly_spelled_words)
            replace_list = create_replace_list(word, keys_correctly_spelled_words,
                                               keyboard_dictionary)
            combined_list = drop_list + insert_list + swap_list + replace_list
            combined_list = list(set(combined_list))  # remove duplicates

            list_of_tuples = []
            for candidate in combined_list:
                list_of_tuples.append((dictionary[candidate], candidate))

            list_of_tuples.sort(reverse=True)

            original_length = len(list_of_tuples)
            length = original_length
            if length > 3:
                length = 3
            if length == 0:
                print("%s -> NOT FOUND" % (justify_right(word, 15)))
            else:
                output_words = ""
                for i in range(length):
                    if i + 1 == length:
                        output_words += list_of_tuples[i][1]
                    else:
                        output_words += list_of_tuples[i][1] + " "
                print("%s -> FOUND%s:  %s" % (justify_right(word, 15),
                                              justify_right(str(original_length), 3),
                                              output_words))


def create_drop_list(word, keys_correctly_spelled_words):
    """Consider all possible ways to drop a single letter from the word.

    Create a list of candidate corrections by considering all possible ways
    to drop a single letter from the word. Store any valid words into a list.

    Args:
        word: A string containing the word to be autocorrected.
        keys_correctly_spelled_words: A list containing keys (correctly spelled
         words) from the provided dictionary.

    Returns:
        list: A list containing candidate corrections found by dropping a
        single letter from the word.
    """
    sublist = []
    for i in range(len(word)):
        char_list = [char for char in word]
        char_list.pop(i)  # Remove character from the list.
        s = char_list_to_string(char_list)
        if s in keys_correctly_spelled_words:
            sublist.append(s)
    return sublist


def create_insert_list(word, keys_correctly_spelled_words):
    """Consider all possible ways to insert a single letter into the word.

    Create a list of candidate corrections by considering all possible ways
    to insert a single letter into the word. Store any valid words into a list.

    Args:
        word: A string containing the word to be autocorrected.
        keys_correctly_spelled_words: A list containing keys (correctly spelled
         words) from the provided dictionary.

    Returns:
        list: A list containing candidate corrections found by inserting a
        single letter into the word.
    """

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    sublist = []
    for alpha in range(len(alphabet)):
        for i in range(len(word) + 1):
            if i == 0:
                insert = alphabet[alpha] + word[i:]
            else:
                insert = word[0:i] + alphabet[alpha] + word[i:]
            if insert in keys_correctly_spelled_words:
                sublist.append(insert)
    return sublist


def create_swap_list(word, keys_correctly_spelled_words):
    """Consider all possible ways to swap two consecutive letters from the word.

    Create a list of candidate corrections by considering all possible ways
    to swap two consecutive letters from the word.
    Store any valid words into a list.

    Args:
        word: A string containing the word to be autocorrected.
        keys_correctly_spelled_words: A list containing keys (correctly spelled
         words) from the provided dictionary.

    Returns:
        list: A list containing candidate corrections found by swapping
        two consecutive letters from the word.
    """
    sublist = []
    char_list_original = [char for char in word]

    for i in range(len(char_list_original) - 1):
        char_list = char_list_original.copy()
        a = char_list[i]
        b = char_list[i + 1]
        char_list[i] = b
        char_list[i + 1] = a

        s = char_list_to_string(char_list)
        if s in keys_correctly_spelled_words:
            sublist.append(s)

    return sublist


def create_replace_list(word, keys_correctly_spelled_words, keyboard_dictionary):
    """Consider all possible ways to replace a single letter into the word.

    Create a list of candidate corrections by considering all possible ways
    to change a single letter in the word with any other letter from the
    possible replacements in the keyboard file.

    Args:
        word: A string containing the word to be autocorrected.
        keys_correctly_spelled_words: A list containing keys (correctly spelled
         words) from the provided dictionary.
        keyboard_dictionary: Python dictionary mapping letters to the
            surrounding keys that are around each letter on the keyboard.

    Returns:
        list: A list containing candidate corrections found by changing a
        single letter in the word with any other letter from the possible
        replacements in the keyboard file.
    """
    sublist = []
    char_list_original = [char for char in word]
    for i in range(len(char_list_original)):
        char_list = char_list_original.copy()
        surrounding_chars = keyboard_dictionary.get(char_list[i])
        if surrounding_chars:
            for j in range(len(surrounding_chars)):
                char_list[i] = surrounding_chars[j]
                s = char_list_to_string(char_list)
                if s in keys_correctly_spelled_words:
                    sublist.append(s)
    return sublist


def get_surrounding_keys(keyboard_file):
    """Read provided keyboard file into a python dictionary.

    Args:
        keyboard_file: A text file containing a letter and the keys that
        surround that letter on a physical keyboard. Contains one line
        for each letter in the alphabet.

    Returns:
        dict: A dict mapping a letter to the surrounding keys that are
            around each letter on the keyboard.
    """
    keyboard_dictionary = dict()
    f1 = open(keyboard_file, 'r')  # keyboard_file | This is the general subin

    for line in f1:
        # Loop through each string in keyboard.txt
        surrounding_keys_list = []
        surrounding = line[2: len(line)]
        for letter in surrounding:
            # find and add the surrounding keys that are around each letter on keyboard
            if letter.isalpha():
                surrounding_keys_list.append(letter)
        keyboard_dictionary[line[0]] = surrounding_keys_list
    f1.close()
    return keyboard_dictionary


def char_list_to_string(char_list):
    """Combine a list of characters into a single string.

    Args:
        char_list: A list of single characters.

    Returns:
        string: A single string containing the characters.
    """
    s = ""
    for c in char_list:
        s += c
    return s


def justify_right(string, full_length):
    """Adjust a string to be right aligned within a specified length.

    Args:
        string: The input string to right-align.
        full_length: The total length the resulting string should have after
            right alignment.

    Returns: A right aligned string with padded spaces on the left.
    """
    l = len(string)
    num_of_spaces_to_pad = full_length - l
    for i in range(num_of_spaces_to_pad):
        string = " " + string
    return string


if __name__ == "__main__":
    #Read input files from the user.
    dictionary_file, input_file, keyboard_file = get_files()

    #Read the keyboard file into a Python dictionary.
    keyboard_dictionary = get_surrounding_keys(keyboard_file)

    #Read in the English dictionary file into a Python dictionary.
    english_dictionary = get_dictionary(dictionary_file)

    #Attempt to autocorrect each word in the input file. Display results.
    auto_correct_file(english_dictionary, input_file, keyboard_dictionary)