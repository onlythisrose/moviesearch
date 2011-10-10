
__author__="Mike Chamberlin"
__author__="Bethany Wickham"
__author__="Daniel Zhao"
__date__ ="$Sep 30, 2011 7:15:21 PM$"


#import abc
#from urllib2 import urlopen
from SearchBase import SearchBase
#from xgoogle.BeautifulSoup import BeautifulSoup

#tagline for the cause that will append to the search results
tagline = '   ***DONATE TO SUPPORT INDEPENDENT FILM!***'

class MovieSearch(SearchBase):
    results = None
    keywords = {}
    searchResults = []

    def search(self, query, rpp):
        self.results = super(MovieSearch, self).search(query, rpp)
        self.reorder()
        self.printResults()

    def printResults(self):
        for res in self.searchResults:
            print res[0].title.encode("utf8")
            print res[0].desc.encode("utf8")
            print res[0].url.encode("utf8")
            if res[1] <> 0:
                print tagline
            print

    def dictionarylist(self):
        key_file = open("keywords.txt",'r')
        count = 1
        for line in key_file:
            for word in line.split():
                self.keywords[word]=count
                count = count+1


    #add by Daniel
#    def getMeta(self, urlline):
#        monty_vid = urlopen(urlline)
#        pageinfo = BeautifulSoup(monty_vid)
#        meta = {}
#
#        meta['title'] = meta['title'] = pageinfo.head('meta')[0]['content']
#        meta['description'] = pageinfo.head('meta')[1]['content']
#        meta['keywords'] = pageinfo.head('meta')[2]['content'].split(', ')
#
#        print meta['title']
#        print meta['description']
#        print meta['keywords']
#        print
#
    
    
    def reorder(self):
        self.dictionarylist()
        value = 0
        orders = []
        pair = ()

        #A boolean variable to record if the search words has matched dictionary
        showlink = False

        #search titles and descriptions for keywords, then append a value to the search result
        for res in self.results:
            tmpTitle = (res.title.encode('utf-8').lower().strip('().,:-\'\"')).split(" ")
            tmpDesc = (res.desc.encode('utf-8').lower().strip('().,:-\'\"')).split(" ")
            #self.getMeta(res.url.encode('utf-8'))


            for key in self.keywords.keys():
                for t in tmpTitle:
                    if key == t:
                        value+=self.keywords[key]
                        showlink = True
                for t in tmpDesc:
                    if key == t:
                        value+=self.keywords[key]
                        showlink = True
            pair = res, value
            orders.append(pair)
            pair = ()
            value = 0

        #order results based on values
        def cmpfun(a,b):
            return cmp(b[1],a[1])
        orders.sort(cmpfun)

#        for i in orders:
#            print i
#            print
#            if i[1] <> 0:
#                print tagline
#            print i[0].title.encode("utf8")#, "RANK = ", i[1]
#            print i[0].desc.encode("utf8")
#            print i[0].url.encode("utf8")
#            print
        #if the search term is not related to keywords
        if showlink == False:
            print "Sponsored Link: http://www.imdb.com/sections/indie/"
            print "Follow Independent Movies on IMDB"
            print

        self.searchResults = orders


