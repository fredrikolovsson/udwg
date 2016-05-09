#!/usr/bin/env python

import sys
from bs4 import BeautifulSoup
import urllib.request as urllib

###############################################################################
# Urban dictionary wordlist generator
#
# gets all most popular words from A-Z 
###############################################################################
class UDWG(object):
    def __init__(self):
        # all possible letters A-Z
        self.letters = list(map(chr, range(65,91)))
        # get only the most popular words
        self.urlprefix = "http://www.urbandictionary.com/popular.php?character="
        self.table = self.getWordsTable()
        # pretty print the table for all words
        self.pprint()

    # takes url and returns soup object
    # in case of failure None returned
    def soupify(self,url):
        try:
            response = urllib.urlopen(url)
        except Exception as e:
            print(e)
            return None
        else:
            html = response.read()
            soup = BeautifulSoup(html)
            return soup

    # returns letter to word table
    # dictionary key letter -> value words list
    def getWordsTable(self):
        table = {}
        for letter in self.letters:
            soup = self.soupify(self.urlprefix+letter)
            table[letter] = self.soup2words(soup)
        return table

    # take soup and return word list
    # empty list returned if soup is None
    def soup2words(self,soup):
        words = []
        # if soup is None return empty list
        if not soup:
            return words
        ul = soup.findAll('ul', attrs={'class':'no-bullet'})
        for listitems in ul:
            for word in listitems.getText().split('\n'):
                if word:
                    words.append(word)
        return words

    # pretty print Urban Dictionary words in table
    # one item per line to standard output 
    def pprint(self):
        for letter in self.letters:
            words = self.table[letter]
            for word in words:
                print(word)

# create UDWG class and pretty print all the words 
# gets only most popular from A-Z
if __name__ == "__main__":
    udwg = UDWG()
