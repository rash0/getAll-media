from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# from django.shortcuts import render_to_response
# from django.template.loader import render_to_string
from selenium import webdriver
import re
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from django.views.decorators.cache import cache_page
import json
import time
import requests

@cache_page(1300)
def index(req, username):

    url = f'https://twitter.com/{username}'

    # check if the user exixts on twitter
    r = requests.get(url)

    if len(username) > 15 or r.status_code != 200 :
        return JsonResponse({ 'message': 'Sorry user canot be found :(' })
    else:

        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)

        driver.get(url)

        res = driver.execute_script('return document.documentElement.outerHTML')
        # length_of_page = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page")
        # match = False
        #
        # while(match==False):
        #     end_of_page = length_of_page
        #     time.sleep(2)
        #     length_of_page = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page")
        #     if end_of_page == length_of_page:
        #         match = True
        #
        # soup = BeautifulSoup(driver.page_source, "html.parser")
        soup = BeautifulSoup(res, "lxml")
        driver.quit()

        # Remove the word 'u-hidden' from the img class, to show the photos that is "senstive" and hidden
        cleanSoup = BeautifulSoup(str(soup).replace("u-hidden", ''), "lxml")

        # get the parent div for twitter stream
        timeline = cleanSoup.find('div', class_ = 'stream')

        # every tweet is made of li element
        tweets = timeline.findAll('li', class_= 'js-stream-item stream-item stream-item')

        # filter the li elemnts that have media only and add them to tweets_with_media
        tweets_with_media = []
        for li in tweets:
            imgs = li.find('img', src=re.compile(".twimg.com/media/"))
            if imgs is not None:
                tweets_with_media.append(li)

        # Function that takes inline-style string and extract the video/gif link from
        # and manipulate it, by removing the word 'thumb' and replacing the word 'jpg' with 'mp4'
        def video_link(link):
            if link != None:
                # Extract the link
                a = str(link).split('\'')[1]
                # Replace the word 'thumb' with nothing
                b = re.sub(r'((_thum))\w+', '', a)
                # Replace the word 'jpg' with 'mp4'
                c = re.sub(r'((jp))\w+', 'mp4', b)
                return c
            else:
                return None

        # init the final dictionary
        results = {}
        results['data'] = []
        
        # Iterate over all the li element inside the div with class "stream"
        for i, li_attr in enumerate(tweets_with_media):

           # Search inside every tweet/li element for the unix time span tag
           tweeted_At = li_attr.find('span', class_ = '_timestamp js-short-timestamp')

           # Twitter doesnt load the gif string before scrolling to it
           videos = li_attr.find('div', class_ = 'PlayableMedia-player')

           images = li_attr.findAll('img', src=re.compile(".twimg.com/media/"))

           if images or videos is not None:
               # Create the first level of the dictionary, which is the tweet ID
               results['data'].append({
                    'tweet_Id': li_attr['data-item-id'],
                    'imgs': [],
                    # Condition in case that the tweet doesnt have videos/gif, then write none instead
                    'videos': video_link(videos),
                    'tweeted_At': tweeted_At['data-time'] if tweeted_At != None else None})
                    # 'created_At': strftime("%d-%b-%Y %H:%M:%S +0000", gmtime())})

               for k, img_attr in enumerate(images):
                   # Create and insert the second level of data, which is an array of images
                   results['data'][i]['imgs'].append(img_attr['src'])


        # Get the path name from the inputed url, to use it for renaming th file
        # a = urlparse(url)
        # account_name = a.path.split('/')[1]

        return JsonResponse(results)



# TO DO Fix the image OR video thing and dont make image when empty give array, but null
# Make pagination for the api...as in scrap first 10 or 20 and then put the rest to the second page and go on
