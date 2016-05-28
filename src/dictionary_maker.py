""" The purpose of this script is to take in three separate newline-delimited text files and combine them into an OWL3
Dictionary approximation. This will involve concatenating them and then alphabetizing and removing duplicates. The three
separate sources are the OSPD4, the new to OWL3 words and the words expurgated in the OSPD5.
"""

import os  # access to systems primitives

__author__ = 'Sonya'
__email__ = "sdsawtelle@gmail.com"
__version__ = "2.7.8"


# First change the working directory to the hardcoded directory where we will keep these three .txt files and ONLY
# those files. In the future this could use argv to take a directory as input and just use the hardcoded values as
# the default if the script is run without any extra parameters (see here:
# http://learnpythonthehardway.org/book/ex15.html).

# Hardcode where the textfiles are kept and change to that directory
path = "C:\Users\Sonya\Dropbox\Shared_SDS_WDB\ScrabbleWords\DictionaryLists"
os.chdir(path)
print os.getcwd()

# os.walk walks the input directory and for each dir rooted there (starting with the input directory itself) it returns
# a tuple of path,dirname,filenames. Note that next(iterator) is equivalent to iterator.next() and both just call the
# _next_ method of the iterator
sources = next(os.walk(path))[2]

print os.path.dirname(path)

# Loop through the list of text sources and for each one open it and read it into a list of words assuming the words are
# delimitd by newlines. The list of words for each file is stored as an element of the list wordlists. Note that
# using with x as open(y) will automatically close the file after executing the nested statements.

# This is elegant but doesn't close files!
# wordlists = [text.readlines() for text in [open(files) for files in sources]]

sourcelists = []
for textfile in sources:
    with open(textfile) as text:
        sourcelists.append(text.readlines())

# Flatten the list of wordlists into one long list of words
words = [word.strip('\n\r') for wordlist in sourcelists for word in wordlist]

# Remove duplicate words by creating a set object from the list object, but then convert it back to a list again!
# Note that going to a set is not order preserving, but that's OK.
full_dictionary = list(set(words))

# Alphabetize the list with sort method - remember that it modifies your list in place! Then output this as a
# newline-delimited text file. This is our official dictionary without any length restrictions.
full_dictionary.sort()
with open("C:\Users\Sonya\Dropbox\Shared_SDS_WDB\ScrabbleWords\OWL3_Dictionary.txt",'w') as text:
    text.writelines(["%s\n" % item for item in full_dictionary])


# # Now remove all the words whose length is more than seven, this will be our official list for the anagram game.
short_dictionary = [word for word in full_dictionary if len(word) <= 7]
with open("C:\Users\Sonya\Dropbox\Shared_SDS_WDB\ScrabbleWords\OWL3_WordsLengthSevenOrLess.txt",'w') as text:
    text.writelines(["%s\n" % item for item in short_dictionary])


print
