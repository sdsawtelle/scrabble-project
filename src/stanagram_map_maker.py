""" This script takes in the length-seven-or-less dictionary that is output by dictionary-maker.py and it creates a
mapping that associates every unique standard anagram with the list of words that it anagrams (unscrambles) to. The
standard anagram of a word is simply the string which is all the characters of the word arranges alphabetically. For
example, "EMBRACE" -> "ABCEEMR"
"""

import os  # access to systems primitives
import operator  # operators and dot-referenced methods/attributes in function-form

__author__ = "Sonya"
__email__ = "sdsawtelle@gmail.com"
__version__ = "2.7.8"


# First change to the working directory and then read in the dictionary file which contains all the words of length
# seven or less.
path = "C:\Users\Sonya\Dropbox\Shared_SDS_WDB\ScrabbleWords"
os.chdir(path)

# Read the file into a list where each line is an element, and strip the newline characters.
with open(path + "\OWL3_WordsLengthSevenOrLess.txt") as text:
    dictionary = text.readlines()
    dictionary = [word.strip("\n") for word in dictionary]


# What we would like to ultimately create is a mapping from each unique stanagram to the list of words that it can make
# (and we only care about stanagrams which actually do make a word). Such a mapping will constitute some kind of
# array-like data structure. Since we want to make looking up stanagrams easy, and since each stanagram will be
# represented only once in this array, we can use a dictionary where the key is the stanagram! We'd like our stanagrams
# to be all capitalized letters, and to be represented by a single string rather than a list of characters.

# We'll start by making the separate stanagram list and formatting it the way we want.
stanlist = map(sorted, dictionary) # Rearrange the characters of each word into the standard anagram.
stanlist = ["".join(stan) for stan in stanlist] # Flatten the lists of capitalized characters into single strings
stanlist = map(operator.methodcaller("upper"), stanlist) # Capitalize all the letters

# Some words map to the same stanagram (like "cat" and "act" both map to "ACT") so first lets get a list of unique
# stanagrams by taking advantage of the set data type.
uniquestans = list(set(stanlist))

# Our final mapping can take the form of a dictionary which we create from a list. First we will initialize our
# stanagram map by associating an empty list with each unique stanagram. Then we convert to a dictionary.
stanmap = [[ustan, []] for ustan in uniquestans]
stanmap = dict(stanmap)

# Now for each unique stanagrams we would like to create a list of words that have that stanagram. That list will be
# entry in the dictionary corresponding to that unique stanagram key value. We can do this by looping through the
# dictionary, computing the stanagram for a word, using that stanagram as a key to look up the corresponding entry in
# the dicitonary, and then appending to the word to that entry.
for word in dictionary:
    # Compute the stanagram for the word
    wordstan = "".join(sorted(word.upper()))
    # Use the stanagram as a lookup key in the dictionary and append the word to that entry
    stanmap[wordstan].append(word);

# Now write the mapping to a comma-delimited text file
with open(path + "/Stanagram_Map.txt", 'w') as text:
    text.writelines(["%s, %s\n" % (key, " , ".join(stanmap[key])) for key in stanmap])


# Finally, we will write a file in python syntax that defines the dictionary mapping object item by item

with open(path + "/stanagram_map.py", 'w') as text:
    text.writelines("__author__ = 'Sonya'\n")
    text.writelines("__email__ = 'sdsawtelle@gmail.com'\n")
    text.writelines("__version__ = '2.7.8'\n\n")
    text.writelines("stanmap = {")
    text.writelines(["'%s': ['%s'], " % (key, "' , '".join(stanmap[key])) for key in stanmap])
    text.writelines("}")

print