# scrabble-anagrams-and-wordlists
The goals of this project are to use the most recent Official Word List (OWL) for Scrabble Tournament plan to 
1. Create some useful word lists that could be made into a cheat sheet, and
2. Build an anagramming console game. 

I used Python 2.7 in the PyCharm IDE. The final outputs are a scrabble cheat sheet PDF that draws from the wordlists and a console game that presents you with a random draw of seven tiles (a scrabble rack) and then can show you the anagramming solution which is all the words that you can make with this rack. As you might imagine, handling blank tiles (wildcards) was the least straightforward part of this project!

[Example of Anagram Console Game Session.](example_game_session.ipynb)

## Scrabble Word Lists
For some reason the OWL3 is not publicly available online, so the first script in this project, `dictionary_maker.py`, recreates the OWL3 as the union of several different lists (the OWL2, the words that are new in the OWL3, and the dirty words that were removed from OWL3 to make the Official Hasbro-endorsed dictionary). This script outputs the final OWL3 as a newline-delimited text file.

The second script `wordlist_maker.py` reads in the dictionary and then filters through it to make different word lists that are useful for serious scrabble players. These include the Q-without-U words and the words with at least 75% vowels. These lists all get output as their own .txt files, but I also combined them into a compact cheat sheet PDF.

## Scrabble Anagram Game
The third file, `stanagram_map_maker.py`, uses the OWL3 text file to create a Python dict that maps every standard anagram to it's list of words that it can make. A standard anagram ('stanagram') for a word or set of letters is simply the alphabetized list of characters. For instance "word" stanagrams to "DORW". Obviously this mapping doesn't bother to include stanagrams that can't make any words, e.g. "CCLP". Finally, this python script actually writes another python script in which the stanagram map dict object is hardcoded line by line to be imported as a module in the actual game script.

The final file, `anagram_console_game.py` imports the `stanagram_map.py` module mentioned above so that it can use the stanagram map dict object to find the solution for a randomly generated rack (set of seven tiles). The conosle game just presents a simple menu that lets you repeatedly receive a new random rack and view the solutions. There was a little bit of non-triviality in how to deal with racks that have a blank tile, or god forbid, two blank tiles!