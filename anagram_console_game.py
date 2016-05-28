""" This script runs a simple console version of the anagram game. The game consists of presenting the user with a
random draw from the full set of scrabble tiles, and then presenting the 'solution' to the rack on-demand. The solution
is the list of all words that can be made with that rack.
"""

import os  # access to systems primitives
import random as rand  # access to random sampling
import itertools as itt  # access to combinatorics stuff for subset generation
import stanagram_map as maps  # access the standard anagram mapping created by standard_map_maker.py

__author__ = 'Sonya'
__email__ = "sdsawtelle@gmail.com"
__version__ = "2.7.8"


class Game:
    ''' Constitutes a session of gameplay - serves up the menu and responds with a rack, the rules or exit'''
    bagtiles = 2*["*"] + 9*["A"] + 2*["B"] + 2*["C"] + 4*["D"] + 12*["E"] + 2*["F"] + 3*["G"] + 2*["H"] + 9*["I"] + 1*["J"] + 1*["K"] + 4*["L"] + 2*["M"] + 6*["N"] + 8*["O"] + 2*["P"] + 1*["Q"] + 6*["R"] + 4*["S"] + 6*["T"] + 4*["U"] + 2*["V"] + 2*["W"] + 1*["X"] + 2*["Y"] + 1*["Z"]

    def __init__(self):
        self.exit = False

    def menu(self):
        print "---------------------------------------------------------"
        print "---------------------------------------------------------"
        print "(1) See Rules"
        print "(2) Play!"
        print "(3) Exit"
        choice = raw_input("What is your choice? (enter a number)")

        if choice == "1":
            self.printrules()
        elif choice == "2":
            self.play()
        elif choice == "3":
            self.exit = True
        else:
            print "Not a valid choice you fool!"
            self.menu()

    def play(self):
        newrack = Rack(self.bagtiles)
        newrack.printrack()
        print "This rack can make ", len(newrack.solution), " different words of length three or more."
        raw_input("Please hit enter when you are ready to see the solutions...\n")
        newrack.printsolution()

    def printrules(self):
        print "---------------------------------------------------------"
        print "You will be presented with a first-turn scrabble rack (a draw of seven tiles from a fresh bag of all the tiles)."
        print "Your job is to figure out all the words of length three or more that can be made with your rack!"
        print "An asterisk (*) indicates a blank tile i.e. a wildcard."


class Rack:
    ''' Constitutes one seven-letter draw from scrabble tiles and has all the corresponding anagram solutions.'''
    def __init__(self, bagtiles):
        self.racktiles = rand.sample(bagtiles, 7)
        self.solution = self.__findsolution__()

    def __findsubsets__(self, tiles):
        ''' returns a list of all unique subsets of length 2 or more from the length-seven list self.racktiles'''

        # check if there are any blank tiles - if so, we need to do some magic we'll work with a sorted version of
        # racktiles and use it to compute subsets, this allows us to assume the blanks will be in the front of the list.
        sortrack = "".join(sorted(tiles))
        alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        if "**" in sortrack:
            # We'll create a list of all possible racks by replacing "**" with "lett1 lett2" where the latter is every possible
            # unique two-letter pair.
            alphabet_twos = ["".join(pair) for pair in itt.combinations_with_replacement(alphabet, 2)]
            possible_racks = [sortrack.replace("**", pair) for pair in alphabet_twos]
            subs = [self.__findsubsets__(list(rack)) for rack in possible_racks]
            # now flatten the list of lists and remove duplicates
            subs = [combo for templist in subs for combo in templist]
            subs = list(set(subs))
        elif "*" in sortrack:
            possible_racks = [sortrack.replace("*", letter) for letter in alphabet]
            subs = [self.__findsubsets__(list(rack)) for rack in possible_racks]
            # now flatten the list of lists and remove duplicates
            subs = [combo for templist in subs for combo in templist]
            subs = list(set(subs))
        else:
            subs = list()
            for length in range(2, 8, 1):
                # get a list of all possible subsets of this length from the set of racktiles
                templist = [sorted(combo) for combo in itt.combinations(tiles, length)]
                # transform into stanagram format for use as keys in the stanagram map, then get unique subsets
                templist = ["".join(combo).upper() for combo in templist]
                subs.append(templist)
            # now flatten the list of lists and remove duplicates
            subs = [combo for templist in subs for combo in templist]
            subs = list(set(subs))
        return subs

    def __findsolution__(self):
        ''' uses the list of all unique subsets and from the standard anagram map returns the list of possible words'''
        subsets = self.__findsubsets__(self.racktiles)
        solution = []
        for stanagram in subsets:
            try:
                solution.append(maps.stanmap[stanagram])
            except KeyError:
                pass

        # now flatten the list
        solution = [word for templist in solution for word in templist]
        # now remove two letter words since that is super easy!
        solution = [word for word in solution if len(word) > 2]
        return solution

    def printrack(self):
        print "---------------------------------------------------------"
        print("This rack has the following tiles:")
        print("".join(self.racktiles))

    def printsolution(self):
        print("This rack can make the following words (length three or more):")
        # Print out the solution words grouped by length (skip lengths that have no words)
        for length in range(3,8,1):
            wordsbylength = [word for word in self.solution if len(word) == length]
            if len(wordsbylength) > 0:
                print wordsbylength


def main():
    ''' This is the main program function that allows for the creation of one instance of class Game.'''
    print "---------------------------------------------------------"
    print "-----  Welcome to the Anagram Game -----"

    newgame = Game()

    while(not newgame.exit):
        newgame.menu()

    print "---------------------------------------------------------"
    print "-----  Goodbye -----"
    print "---------------------------------------------------------"

    return


main()
