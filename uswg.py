#!/usr/bin/python


#http://www.urbandictionary.com/browse.php?character=A
#http://www.urbandictionary.com/browse.php?character=*
#http://www.urbandictionary.com/browse.php?character=A&page=413
#if page number is too large, it redirects to initial page

class UDScraper():
    def __init__(self):
        #page letters + * for non-alphabetic words
        self.letters = map(chr, range(65,91)) + ["*"]
        #scraped pages
        self.pages = self._getPages()
        #extracted terms
        self.terms = self._getTerms()
    
    #TODO: returns a page for a given letter and page number
    def _getPage(self, letter, pageNumber):
        #if page redirects, return null?
        ##should extract terms here to save space
        return ""

    #returns a list full of pages
    def _getPages(self):
        list_of_pages = []
        pageNumber = 0
        for letter in self.letters:
            page = self._getPage(letter, pageNumber)
            while(page != ""):
                list_of_pages.append(page)
                pageNumber += 1
                page = self._getPage(letter, pageNumber)
        return list_of_pages

    #returns a dictionary of terms
    def _getTerms(self):
        list_of_terms = []
        for page in self.pages:
            list_of_terms.extend(self._extractTerms(page))
        for term in list_of_terms:
            if term not in self.terms:
                self.terms[term] = term

    #TODO: extract terms from a given page and return a list for that page
    def _extractTerms(self, page):
        return []

    #print self.terms
    def printWordList(self):
        for term in self.terms:
            print term

#start main()
if __name__ == "__main__":
    udscraper = UDScraper()
    udscraper.printWordlist()

