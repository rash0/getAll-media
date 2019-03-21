from django.http import HttpResponse
from django.shortcuts import render
# from django.shortcuts import render_to_response
# from django.template.loader import render_to_string
from selenium import webdriver
import re
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from django.views.decorators.cache import cache_page


def index(req, username):
    # if request.method == 'POST':
    print(username)
    # else:
    #     print('no requests found')
    # return render(req, 'app.html',context)

@cache_page(1300)
def scrap(request):
    # Clean the input
    # options = Options()
    # options.headless = True
    # driver = webdriver.Firefox(options=options)
    # # driver = webdriver.Firefox()
    # driver.get('https://twitter.com/aestheticsweeb')
    # res = driver.execute_script('return document.documentElement.outerHTML')
    # soup = BeautifulSoup(res, "html.parser")
    # driver.quit()
    #     # get the parent div for twitter stream
    # timeline = soup.find('div', class_ = 'stream')
    #
    # # every tweet is made of li element
    # tweets = timeline.findAll('li', class_= 'js-stream-item stream-item stream-item')
    #
    # results = []
    #
    # for i, li_attr in enumerate(tweets):
    #
    #        results.append({'imgs': []})
    #
    #        for k, img_attr in enumerate(li_attr.find_all('img', src=re.compile(".twimg.com/media/"))):
    #        # Create and insert the second level of data, which is an array of images
    #             results[i]['imgs'].append(img_attr['src'])
    #
    # context = {
    #     'result_data': username
    # }
    print(request.GET['username'])
    return  render(request, 'index.html')
    # return HttpResponse(soup)
