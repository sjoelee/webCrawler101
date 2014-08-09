import urlparse
import urllib
from bs4 import BeautifulSoup

url = "http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes"

#url = "http://www.yellowpages.com/tucson-az/mip/cupcakes-456735205?lid=456735205"

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
    for tag in soup.findAll('a', class_="business-name"):
        if tag.span:
            businessNames.append(tag.span.renderContents())
            print tag.span.renderContents()

    print "Number of busineses on this page:", len(businessNames)
        
