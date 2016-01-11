import time
import re
import os
import logging
from datetime import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
#from db import flixrdb
#from couch import db
#from webdriver_util import init, wait_and_get
    

class Flixr:
    def __init__(self):
        self.driver = webdriver.Firefox()
        #self.driver, self.waiter, self.selector = init()
        #wait_and_get(self.driver,url)
        self.start=datetime.utcnow()
        self.stop = datetime.utcnow()
        self.title = []
        self.posterurl = []
        self.movieurl = []
        self.movieinfo = []
        self.releasedates = []
        self.trailer = []
        self.rated = []
        self.genre = []
        self.director = []
        self.cast = []
        self.duration = []
        self.get_future_movie_times()
        self.get_upcoming_movies_info()
        self.driver.close()
        flixrdb.close()
   
    def get_future_movie_times(self):
        #driver, waiter, selector = init()
        #print 'driver started'
        #print 'wait and get done'
        url = 'https://www.amctheatres.com/advance-tickets'
        self.driver.get(url)
        html = self.driver.page_source
        #driver.quit()
        soup = BeautifulSoup(html)
        table = soup.findAll('div',{"class":"poster"})
        for x in table:
            tags = x.find('a')
            imgtag = tags.find('img')
            self.posterurl.append(imgtag.attrs['src'])
            movie = str('http://www.amctheatres.com'+tags.attrs['href'])
            self.movieurl.append(movie)


    def get_upcoming_movies_info(self): 
        moviekey = 0  
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('fl.log')
        logger.addHandler(handler)
        logger.info(datetime.utcnow())
        monthdayRE = re.compile("[A-Z][a-z]+ \d+, \d+")
        movielenRE = re.compile("\d [a-z][a-z] \d+ [a-z][a-z][a-z]")
        #self.driver, waiter, selector = init()
        for x in self.movieurl:
            #wait_and_get(self.driver,x)
            self.driver.get(x)
            #driver.get(x)
            html = self.driver.page_source
            soup = BeautifulSoup(html)
            medposter = soup.find()
            table = soup.findAll('dl',{"class":"dl-horizontal"})
            genre = soup.find('dd',{"itemprop":"genre"})
            rate = soup.find('span',{"itemprop":"contentRating"})
            trailer = soup.find('a',{"class":"trailer-modal"})#trailer-modal btn btn-alt btn-action btn-sm
            director = soup.find('dd',{"itemprop":"director"})
            cast = soup.find('dd',{"itemprop":"actors"})
            title = soup.find('span',{"itemprop":"name"})

            try:
                self.title.append(title.string)       
            except Exception as e:
                self.title.append("Title not available")
                     
            try:
                self.director.append(director.string)
            except Exception as e:
                self.director.append("Director not available")

            try:
                self.cast.append(cast.string)
            except Exception as e:
                self.cast.append("Cast not available")

            try:
                self.trailer.append(str(trailer['href']))
            except Exception as e:
                self.trailer.append("Trailer not available")

            try:
                self.genre.append(genre.string)
            except Exception as e:
                self.genre.append("Genre not available")

            try:
                self.rated.append(rate.string)
            except Exception as e:
                self.rated.append("Rating not available")

            for i in table:
                lvc = ''
                tagss = i.find_all('dd')
                for x in tagss:
                    lvc = lvc + str(x.string)
                releasedates=re.findall(monthdayRE,lvc)
                duration = re.findall(movielenRE,lvc)
                self.duration.append(duration)
                self.releasedates.append(releasedates)

            logger.info(self.title[moviekey])


            #doc_id, doc_rev = db.save({'_id':self.title[moviekey],'cast':self.cast[moviekey],'director':self.director[moviekey],'duration':self.duration[moviekey],'rated':self.rated[moviekey],'trailer':self.trailer[moviekey],'title':self.title[moviekey],'releasedate':self.releasedates[moviekey], 'poster':self.posterurl[moviekey]} )
            #flixrdb[self.title[moviekey]] = {'cast':self.cast[moviekey],'director':self.director[moviekey],'duration':self.duration[moviekey],'rated':self.rated[moviekey],'trailer':self.trailer[moviekey],'title':self.title[moviekey],'releasedate':self.releasedates[moviekey], 'poster':self.posterurl[moviekey]}        
            moviekey = moviekey+ 1

        logger.info(datetime.utcnow())

    def get_meta(self):
        return {'cast':self.cast,'director':self.director,'duration':self.duration,'rated':self.rated,'trailer':self.trailer,'title':self.title,'releasedate':self.releasedates, 'poster':self.posterurl}

if __name__ == "__main__":
    x=Flixr()

   