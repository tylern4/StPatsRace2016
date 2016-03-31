import dryscrape
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

base_url = "http://racesonline.com/events/st-pat-s-in-5-points-get-to-the-green/results/2016?page="

def getwebpage(url):
    session = dryscrape.Session()
    session.visit(url)
    response = session.body()
    return BeautifulSoup(response, "lxml")

def get_data(soups):
    results = []
    bad_results = []
    for link in soups.find_all('tr')[1:]:
        link = str(link)
        #remove extra html tags
        link = link.replace('<td>',' ').replace('</td>',' ')
        #remove tabs and newlines and replace with ','
        link = ','.join(link.split())
        #replace some common city names
        #takes malformed from ~215 to ~97
        link = link.replace('WEST,COLUMBIA','WEST COLUMBIA').replace('ROCK,HILL','ROCK HILL')
        link = link.replace('HILTON,HEAD,ISLAND','HILTON HEAD ISLAND').replace('NORTH,AUGUSTA','NORTH AUGUSTA')
        link = link.replace('SHAW,AFB','SHAW AFB').replace('FORT,JACKSON','FORT JACKSON').replace('FT.,JACKSON','FORT JACKSON')
        #remove begining and end of each line
        link = link[link.find(">,")+2:link.find("/mile")]
        #if the data looks good add it to the results else add it to the malformed list
        if link.count(',') == 13:
            results.append(link)
        else:
            bad_results.append(link)
    return results,bad_results


csv = []
malformed = []
for page in xrange(1,21):
#for page in xrange(1,5):
    url = base_url + str(page)
    results,bad_results = get_data(getwebpage(url))
    csv.extend(results)
    malformed.extend(bad_results)

for p in malformed: print p
print "\n\n"+"Bib,First Name,Last Name,Race,Race Rank,Gender,Gen Rank,Age,Age Group,AG Rank,City,ST,Chip Time,Pace"
for p in csv: print p

