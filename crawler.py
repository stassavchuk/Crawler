import urlparse
import urllib
from bs4 import BeautifulSoup
import thread

def crowl_tutor_page(url):

    htmltext = urllib.urlopen(url).read() # read the page

    soup = BeautifulSoup(htmltext)
    # get name
    name =  soup.findAll('div', { "class":"name" })
    name = name[0].contents[0]

    # get city
    city = soup.findAll('a', {"class":"adr"})
    city = city[0].contents[0]

    # get code
    code = soup.findAll('div', { "class":"col-sm-12 col-md-8" })[1]
    code = code.contents[0].split()[0]

    # get subjects
    # need to optimize
    subjects = soup.findAll('div', {"class":"visible-xs-block clearfix"})
    subjects = subjects[0].contents[1].contents[1].contents
    while '\n' in subjects:
        subjects.remove('\n')
    s = []

    try:
        for sub in subjects:
            s.append(sub.contents[0].contents[0])
    except IndexError:
        s.append("NO SUBJECT")
    subjects = s

    # get data if joined

    # get url of profile
    url_of_profile = url

    # get url of profile picture
    img = soup.findAll('img', {"class":"photo"})
    profile_img = None
    for tag in img:
         profile_img = tag["src"]

    # save to cvs:
        # name
        # city
        # code
        # subjects
        # data if joined
        # url of profile
        # url of profile picture

    print name
    try:
        print city
    except UnicodeEncodeError:
        print "NOT FUCKING UNICODE RELEVANT CITY"

    print code
    print subjects[0]
    print url_of_profile
    print profile_img
    
def crowl_page_with_tutors(url):

    # read the page
    htmltext = urllib.urlopen(url).read()
    soup = BeautifulSoup(htmltext)

    tutors_url = []

    # crowl urls
    for tag in soup.findAll('a'):
        if tag.contents == ['View Tutor']:
            tutors_url.append(tag["href"])

    # clowl each ural
    for x in tutors_url:
        crowl_tutor_page(x)
        
def take_next_page(url):
    try:
        htmltext = urllib.urlopen(url).read()
        soup = BeautifulSoup(htmltext)
        next_page = soup.findAll('a', {"class":"next_page"})[0]["href"]
        return next_page
    except IndexError:
        return None
        
def crowl_the_city(url):
    while True:
        crowl_page_with_tutors(url)
        if take_next_page(url) != None:
            url = take_next_page(url)
        else:
            break
        
def crowl_site_map(url):

    htmltext = urllib.urlopen(url).read() # read the page
    soup = BeautifulSoup(htmltext)

    cities = soup.findAll('ul', {"class" : "sitemap_list"})
    cities = cities[1].contents

    while '\n' in cities:
            cities.remove('\n')
    c = []
    for tag in cities:
        c.append(tag.contents[0]["href"])

    cities = c

    return cities
    
def start_crowl():

    site_map_url = "http://www.universitytutor.com/sitemap"
    cities = crowl_site_map(site_map_url)

    for city in cities:
        crowl_the_city(city)




    # concept of multithreading
    # it doesn't work

    # for city in cities:
    #     try:
    #         thread.start_new_thread(crowl_the_city, (city,))
    #     except:
    #         print "---------------------------"
    #         print "|   PTOBLEM WITH THREAD   |"
    #         print "---------------------------"
