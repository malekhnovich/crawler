import urllib.request
import urllib
import time
from bs4 import BeautifulSoup

# 10 TERMS: 'factory','prototype' 'builder', 'singleton', 'software development',
# 'software programming', 'creational', 'structural', 'behavioral','object-oriented programming',
# SEED URLS: 'https://en.wikipedia.org/wiki/Software_design_pattern',
# 'https://en.wikipedia.org/wiki/Object-oriented_programming'
import sys
sys.setrecursionlimit(100000)
import ssl
#IN ORDER TO AVOID SSL CERTIFICATE ERROR
ssl._create_default_https_context = ssl._create_unverified_context
links=[]
headers = {}
#NEED TO GET DATA FROM WIKIPEDIA:Headers is passed into urllib request
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

def getPageContent(url):
    try:
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        responseText = resp.read()
    except Exception as e:
        print(str(e))
        return None
    soup = BeautifulSoup(responseText, "html.parser")
    return soup

def getLinks(currentPageContent):

    for tag in currentPageContent.findAll('a',href=True):
        tag = tag.get('href')
        if(tag.startswith('//')):
            tag="http://"+tag[2:]
        if(tag.startswith('/')):
            tag = "http://en.wikipedia.org"+tag


        if(tag.startswith('#')==False):
            links.append(tag)
    return links

def writeToRelevantCrawledFile(relevantCrawledWebsites):

    counter=0
    for url in relevantCrawledWebsites:
        resultsFile = open("pageWithSearchTerms"+str(counter)+'.txt', 'w+')
        resultsFile.write("The following page is located at the url: " + url + "\n")
        resultsFile.write(str(getPageContent(url))+"\n")
        resultsFile.close()
        counter+=1
        print("The counter is "+str(counter))

def writeReport(visitedWebsites,relevantVisitedWebsites):
    allResultsFile=open('Report.txt','w+')
    allResultsFile.write(("Topic of my choice is "+topic+"\n"))
    allResultsFile.write("The search terms are: "+str(searchTerms)+"\n")
    allResultsFile.write("The seed URLS are: "+str(seedUrls)+"\n")
    allResultsFile.write("MAX number of pages with relevant information "+str(maxRelevantPagesToFind)+"\n")
    allResultsFile.write("Total Number of visited  pages is: "+str(len(visitedWebsites))+"\n")
    allResultsFile.write("Number of Actually Found relevant pages "+str(len(relevantVisitedWebsites))+"\n")
    allResultsFile.write("Below is a complete list of visited Pages"+"\n")
    for visitedWebsite in visitedWebsites:
        allResultsFile.write("The visited site is "+visitedWebsite+"\n")
    allResultsFile.close()
    
def contains(searchTerm, pageContentText):
    if(searchTerm in pageContentText):
        return True
    else:
        return False

def checkPageForRelevance(pageContent,searchTerms):
    searchTermCount=0
    pageContentText=pageContent.get_text()
    pageContentText=pageContentText.lower()

    for searchTerm in searchTerms:
        searchTerm=searchTerm.lower()
        if(contains(searchTerm,pageContentText)):
            searchTermCount+=1
        if(searchTermCount==2):
            return True
    return False

def processPage(url,searchTerms,visitedWebsites,relevantVisitedWebsites):
    if len(relevantVisitedWebsites)==maxRelevantPagesToFind:
        return
    if url in visitedWebsites:
        return
    visitedWebsites.append(url)
    currentPageContent = getPageContent(url)
    if(currentPageContent==None):
        return
    if(checkPageForRelevance(currentPageContent,searchTerms)):
        if(url not in relevantVisitedWebsites):
            relevantVisitedWebsites.append(url)
            print("found relevant page "+str(len(relevantVisitedWebsites)))

    currentPageLinks = getLinks(currentPageContent)
    for foundUrl in currentPageLinks:
        processPage(foundUrl,searchTerms,visitedWebsites,relevantVisitedWebsites)

def crawl(topWebSites,searchTerms):
    visitedWebsites = list() #empty until we start crawling
    relevantVisitedWebsites=list()
    for topUrl in topWebSites:
        processPage(topUrl,searchTerms,visitedWebsites,relevantVisitedWebsites)
    writeToRelevantCrawledFile(relevantVisitedWebsites)
    writeReport(visitedWebsites,relevantVisitedWebsites)#this is the report


# TOPIC: design patterns
topic = "design patterns"
url1 = 'http://en.wikipedia.org/wiki/Software_design_pattern'
url2 = 'http://en.wikipedia.org/wiki/Object-oriented_programming'
searchTerms = ['factory','prototype','builder','singleton','software development','software programming','creational','structural','behavioral','object-oriented programming']
maxRelevantPagesToFind=500
seedUrls=[]
seedUrls.append(url1)
seedUrls.append(url2)
crawl(seedUrls, searchTerms)



