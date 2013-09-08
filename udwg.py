import sys
import BeautifulSoup
import urllib2

################################################################################
# globals
#
# chars is a list of all possible chars that can be chosen
# char_dict is a dictionary of all possible chars that can be chosen
################################################################################
chars = map(chr, range(65,91)) +  map(chr, range(97,123)) + ["*"]
char_dict = dict(zip(chars,chars))

################################################################################
# soupify returns BeautifulSoup
#
# tries to download the HTML for a URL and returns BeautifulSoup upon success
# otherwise it returns None on failure
################################################################################
def soupify(url):
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        print e
        return None
    except urllib2.URLError as e:
        print e
        return None
    else:
        html = response.read()
        soup = BeautifulSoup.BeautifulSoup(html)
        return soup

################################################################################
# isliEndOfPage returns bool
#
# specific to urban dictionary HTML layout
# checks <li> tag for words "Previous" or "Next"
# if it finds those words, we assume it is the end of the page and return True
# otherwise it is not the <li> tag we are looking for and returns False
################################################################################
def isliEndOfPage(li):
    if "Previous" in li.text or "Next" in li.text:
        return True
    return False

################################################################################
# printWordsOnPage returns NoneType
#
# this function takes the soup of the page and prints out all the words
################################################################################
def printWordsOnPage(soup):
    if soup.li:
        lis = soup.li.findAllNext('li')
        for li in lis:
            if isliEndOfPage(li):
                break
            if li.a:
                if li.a.text:
                    print htmlStringToWord(li.a.text)

################################################################################
# htmlStringToWord returns str
#
# takes reserved character strings from html and returns a "human readable" str
################################################################################        
def htmlStringToWord(htmlString):
    if htmlString:
        return BeautifulSoup.BeautifulSoup(htmlString, convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)

################################################################################
# getPageCount returns int
#
# goes to the end of a page on urban dictionary and returns the page count
################################################################################
def getPageCount(soup):
    lis = soup.li.findAllNext('li')
    count = len(lis)
    i = count - 2
    pages = lis[i]
    if pages.a:
        if pages.a.text:
            return int(pages.a.text)


################################################################################
# udwg returns NoneType
#
# prints out all the words on urban dictionary starting from the first letter
# and ending on the last letter. this also includes '*' as a special character
# for numbers. 
################################################################################
def udwg(firstLetter, lastLetter):
    letters = getLetters(firstLetter, lastLetter)
    for letter in letters:
        soup = soupify("http://www.urbandictionary.com/browse.php?character="+letter)
        if soup:
            printWordsOnPage(soup)
            pageCount = getPageCount(soup)
            if pageCount > 1:
                for p in range(2,pageCount+1):
                    soup = soupify("http://www.urbandictionary.com/browse.php?character="+letter+"&page="+str(p))
                    printWordsOnPage(soup)

################################################################################
# getLetters returns list
#
# returns a list of corresponding letters and '*' for numbers.
# if the first and last letter are available, and inclusive list is returned
# if the last letter is None, a list of one item is returned (first letter)
################################################################################
def getLetters(firstLetter, lastLetter):
    star = '*'
    start = 65
    end = 91
    letters = []
    if firstLetter and lastLetter:
        firstLetter = firstLetter.upper()
        lastLetter = lastLetter.upper()
        if lastLetter == star:
            letters = map(chr, range(ord(firstLetter),91)) + ["*"]
        else:
            letters = map(chr, range(ord(firstLetter),ord(lastLetter)))
    elif firstLetter:
        firstLetter = firstLetter.upper()
        if firstLetter == star:
            letters = [star]
        else:
            letters = [firstLetter]
    else:
        letters = map(chr, range(65,91)) + ["*"]
    return letters

################################################################################
# checkArg returns NoneType
#
# checks the argument in the list argv 
# if the argument in question is not a char or not a known letter, python exits
################################################################################
def checkArg(argv, i):
    if ( len(argv[i]) != 1 ) or ( not char_dict.has_key(argv[i]) ): 
        print "Please specify a letter or '*'."
        print "Argument", str(i), "is not a letter or '*'."
        print "Argument supplied is too long: ", argv[i]
        sys.exit()

################################################################################
# __main__
#
# checks arguments and calls udwg() with corresponding arguments
# if the arguments are faulty, the program will exit with a message
################################################################################
if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 1:
        udwg(None, None)
    elif argc == 2:
        checkArg(sys.argv, 1)
        udwg(sys.argv[1], None)
    elif argc == 3:
        checkArg(sys.argv, 1)
        checkArg(sys.argv, 2)
        udwg(sys.argv[1], sys.argv[2])
