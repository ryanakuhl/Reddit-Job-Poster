import feedparser
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
import time
from random import randint
from slackclient import SlackClient
import praw
import requests
from bs4 import BeautifulSoup

from builtins import any as b_any


reddit = praw.Reddit(user_agent='#', client_id='#', client_secret='#', username='#', password='#')

subreddit=reddit.subreddit('LouisvilleJobs')

#don't repost
list = []
already = []
naughty = ['Open House',
           'Janitor',
           'O/o',
           'Fuel',
           'Uber',
           'Host',
           'Tutor',
           'Intern',
           'Lyft',
           'Hospital',
           'Guaranteed',
           'Retail',
           'Laborer',
           'Owner Operator',
           'Restaurant',
           'Attendant',
           'New Career',
           'Otr',
           'Truck',
           'Mechanic',
           'Receptionist',
           'Kinder',
           'Teacher',
           'Picker',
           'Financial Advisor',
           'Driver',
           'Phlebotomist',
           'Class A',
           'Entry',
           'Cdl',
           'Jewish',
           'Nurs',
           'Part ',
           'Part-',
           'Automotive',
           'Customer Service',
           'Insurance',
           'Assistant',
           'Lvn',
           'Store Manager',
           'Sales Agent',
           'Metlife',
           'Sales Associate',
           'Staffing',
           'Avon',
           'Landscape',
           'Cpm',
           'Hair',
           'Cashier',
           'Clerk',
           'Beauty',
           'Cook',
           'Therapist',
           'Fulfillment',
           'Greeter',
           'Warehouse',
           'Dishwasher',
           'Rn',
           'Lpn',
           'Flatbed',
           'Server']
banned = ['Insurance',
          'Jewish',
          'Hospital',
          'Metlife',
          'Spectrum',
          'Avon',
          'Army',
          'Randstad',
          'Staffmark',
          'Kforce',
          'Integrated Resources',
          'Davita',
          'Talent',
          'Staffing',
          'Metlife',
          'Avon',
          'Amazon',
          'Nseco',
          'Arvato',
          'Nesco',
          'Ulta']

def indeedpost(link,title,summary):
    if link not in list[0:2000]:
        title = title.replace('(Louisville KY)','')
        title = title.replace('(Louisville Ky)','')
        title = title.replace('(Louisville, KY)','')
        title = title.replace('(Louisville, Ky)','')
        title = title.replace('(Louisville)','')
        if title not in already:
            reddit.subreddit('louisvillejobs').submit(title, url=link).reply(summary)
            list.append(link)
            print('Indeed posted\n',title)
            time.sleep(4)

def indeed():
    try:
        feed = feedparser.parse("https://www.indeed.com/rss?as_and=&as_phr=&as_any=&as_not=humana%2C+mercer%2C+marsh&as_ttl=&as_cmp=&jt=fulltime&st=&sr=directhire&salary=%2460k-100k&radius=25&l=Louisville%2C+KY&fromage=1&limit=50&sort=&psf=advsrch")
        for entry in feed.entries[0:10]:
            # gets RSS details
            link = entry.link
            title = entry.title
            title = title.title()
            summary = entry.summary
            published = entry.published
            published = published.replace(' GMT','')
            published = published.replace(' GM','')
            published = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S")
            published = published.replace(tzinfo=None)
            present = datetime.now() - timedelta(minutes=400)
            # if the entry is new-ish and best price v good deal, continue
            if present < published:
                if any(s in title for s in naughty):
                    pass
                elif b_any(title in x for x in already) == True:
                    pass
                else:
                    indeedpost(link,title,summary)

    except:
        print('something went awry with Indeed')
        pass

def clpost(link,title,summary):
    if link not in list[0:2000]:
        title = title.replace('(Louisville KY)','')
        title = title.replace('(Louisville Ky)','')
        title = title.replace('(Louisville, KY)','')
        title = title.replace('(Louisville, Ky)','')
        title = title.replace('(Louisville)','')
        if title not in already:
            reddit.subreddit('louisvillejobs').submit(title, url=link).reply(summary)
            list.append(link)
            print('Craigslist posted\n',title)
            time.sleep(4)

def cl():
    #try:
        feed = feedparser.parse("https://louisville.craigslist.org/search/jjj?employment_type=1&excats=15-85-29&format=rss&postedToday=1&query=-amazon%20-truck%20-uber%20-cpm%20-floater%20-lyft%20%24%20-fullfillment%20-chewy%20-cdl%20-driver")
        for entry in feed.entries[0:10]:
            # gets RSS details
            link = entry.id
            title = entry.title
            title = title.title()
            summary = entry.summary
            published = entry.published
            published = published.replace('T',':')
            published = published.replace('-04:00','')
            published = published.replace('-05:00','')
            published = datetime.strptime(published, "%Y-%m-%d:%H:%M:%S")
            published = published.replace(tzinfo=None)
            present = datetime.now() - timedelta(minutes=200)
            # if the entry is new-ish and best price v good deal, continue
            if present < published:
                if any(s in title for s in naughty):
                    pass
                elif b_any(title in x for x in already) == True:
                    pass
                else:
                    clpost(link,title,summary)
    #except:
        #print('something went awry - Craigslist')
        #pass

def monsterpost(title,company,link):
    if link not in list[0:2000]:
        title = title+' - '+company
        """title = title.replace('(Louisville KY)', '')
        title = title.replace('(Louisville Ky)', '')
        title = title.replace('(Louisville, KY)', '')
        title = title.replace('(Louisville, Ky)', '')
        title = title.replace('(Louisville)', '')"""
        reddit.subreddit('louisvillejobs').submit(title,url=link)
        list.append(link)
        print('Monster posted\n',title)
        time.sleep(4)

def monster():
    try:
        page = requests.get('https://www.monster.com/jobs/search/Full-Time_8?rad=20&where=Louisville__2c-KY&tm=0&jobid=b8e35d2a-01fc-47d3-a11a-5c79d32eb6c8&stpage=1&page=2&page=3&page=4')
        soup = BeautifulSoup(page.text, 'lxml')
        for job in soup.find_all(class_='card-content'):
          title = job.find(class_='title')
          company = job.find(class_='company')
          if company is not None:
            company = company.find(class_='name')
            company = company.text
            company = company.title()
            if company == None:
              pass
            elif title is not None:
              link = title.find('a')
              link = link.get('href')
              title = title.text
              title = title.replace('\n', '')
              title = title.replace('\r', '')
              title = title.title()
              if any(s in title for s in naughty) or any(s in company for s in banned):
                pass
              elif b_any(title in x for x in already) == True:
                pass
              elif link is not None:
                monsterpost(title,company,link)


    except:
        print('something went awry - Monster')
        pass

while True:
    for submission in reddit.subreddit('LouisvilleJobs').new(limit=50):
        already.append(submission.title.title())

    timenow = datetime.now()
    t = datetime.now().strftime('%m %d, at %H:%M:%S')
    print('\nScrolled Monster at',t)
    monster()
    time.sleep(250)
    t = datetime.now().strftime('%m %d, at %H:%M:%S')
    print('\nScrolled Craigslist at',t)
    cl()
    time.sleep(250)
    t = datetime.now().strftime('%m %d, at %H:%M:%S')
    print('\nScrolled Indeed at',t)
    indeed()
    time.sleep(250)
