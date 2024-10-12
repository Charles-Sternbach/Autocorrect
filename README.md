Autocorrect Project:
- A small version of autocorrect that looks for a few common
typographical errors.

How to run the program:
- Provide the following inputs when prompted:

Dictionary file => support_files/words_10percent.txt

Input file      => support_files/input_words.txt

Keyboard file   => support_files/keyboard.txt

- You can change the dictionary file and the input file provided it
meets the same specifications of the original files stated below.

--

To solve this problem, the program will read the names of three files:

[1] A list of valid words and their frequencies - words_10percent.txt
- Contains two entries per line; the first entry on the line is a
single valid word in the English Language. The second entry is a float
representing the frequency of the word in the lexicon. The two values are
separated by a comma.

- The frequency will be used for deciding the most likely correction when
there are multiple possibilities.

[2] A list of words to autocorrect - input_words.txt
- The program will go through every single file in input_words.txt, autocorrect
each word and print the correction.

[3] A list of potential letter substitutions (described below). - keyboard.txt
- keyboard.txt has a line for each letter. The first entry on the line is the
letter to be replaced. The remaining letters are possible substitutions
for that letter. All the letters on the line are separated by spaces.

- These substitutions are calculated based on adjacency on the keyboard,
so if you look down at your keyboard, you will see that the "a" key is
surrounded by "q", "w", "s", and "z".
Other substitutions were calculated similarly.

--

Correcting Words:
To correct a single word, the following will be considered.

[1] FOUND:
- If the word is in the dictionary, it is correct. There is no need
for a change. Print as found, and go onto the next word.

Otherwise, we will consider all of the remaining possibilities:

[2] DROP:
- If the word is not found, consider all possible ways to drop a single letter
from the word. Store any valid words (words that are in our English Dictionary)
in some container. These will be candidate corrections.

[3] INSERT:
- If a word is not found, consider all possible ways to insert a single letter
into the word. Store any valid words in some container. These will be
candidate corrections.

[4] SWAP:
- Consider all possible ways to swap two consecutive letters from the word.
Store any valid words in some container. These will be candidate corrections.

[5] REPLACE:
- Consider all possible ways to change a single letter in the word
with any other letter from the possible replacements in the keyboard file.
Store any valid words in some container. These will be candidate corrections.

--

After going through all of the above, if there are multiple potential matches,
they will be sorted by their potential frequency from the English dictionary
and return the top 3 values that are in most frequent usage as the most likely
corrections in order.

If there are three or fewer potential matches, we will print them all in order.

If there are no potential matches using any of the above corrections,
we will print NOT FOUND. Otherwise, we will print the following on a single line.

[1] The word.

[2] The number of matches.

[3] At most three matches.