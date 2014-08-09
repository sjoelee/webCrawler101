import urlparse
import urllib
from bs4 import BeautifulSoup


#url = "http://www.yellowpages.com/tucson-az/mip/cupcakes-456735205?lid=456735205"

class businessListing():
    def __init__(self, name, streetAddress, city, state, phoneNumber):
        self.name = name
        self.streetAddress = streetAddress
        self.city = city
        self.state = state
        self.phoneNumber = phoneNumber

    def printInfo():
        print "Name: ", self.name
        print " Street Address: %s" % (self.streetAddress)
        print " City: %s, State: %s" % (self.city, self.state)
        print " Phone #: ", self.phoneNumber


def getPageResults(url, soup):
    pageResults = []
    # Store all results into a list
    pageResults.append(url)
    for tag in soup.findAll('a', attrs={"data-remote":"true"}, href=True):
        pageResults.append(urlparse.urljoin(url, tag['href']))

    return pageResults

def main():
    url = "http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes"
    pageResults = []
    urls = [url] # stack of urls to scrape
    visited = [url]
    businessNames = []

    while len(urls) > 0:
        try:
            htmltext = urllib.urlopen(urls[0]).read()
        except:
            print urls[0]
        soup = BeautifulSoup(htmltext)
    
        urls.pop(0)
    
        # What if soup is null?? Need to handle this exception
        pageResults = getPageResults(url, soup)
        print pageResults[0]

        for result in pageResults: # restrict to one listing
            htmltext = urllib.urlopen(result).read()
            soup = BeautifulSoup(htmltext)
            for tag in soup.findAll('a', class_="business-name"):
                if tag.span:
                    businessNames.append(tag.span.renderContents())
                    print tag.span.renderContents()
    
        print "Number of busineses on this page:", len(businessNames)
            
if __name__=="__main__":
    main()
    
