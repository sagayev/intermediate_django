import math
from datetime import datetime, timedelta, timezone

# Create your views here.
import requests
from bs4 import BeautifulSoup
from django.shortcuts import redirect, render

from .models import Headline, UserProfile

#requests.packages.urllib3.disable_warnings()
requests.urllib3.disable_warnings()


def news_list(request):
    user_p = UserProfile.objects.filter(user = request.user).first()
    now = datetime.now(timezone.utc)
    time_difference = now - user_p.last_scrape
    time_diff_in_hours = time_difference / timedelta(minutes=60)
    next_scrape = 24 - time_diff_in_hours

    if time_diff_in_hours < 24:
        hide_me = True
    else:
        hide_me = False

    headlines = Headline.objects.all()
    context = {
        'object_list': headlines,
        'hide_me':hide_me,
        'next_scrape': math.ceil(next_scrape)
    }
    return render(request, "news/home.html", context)

def scrape(request):
    user_p = UserProfile.objects.filter(user = request.user).first()
    user_p.last_scrape = datetime.now(timezone.utc)
    user_p.save()

    session = requests.Session()
    session.headers = { 
        "User-Agent" :
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }
    url = 'https://www.theonion.com/'
    
    content = session.get(url, verify=False).content
    
    soup = BeautifulSoup(content, "html.parser")

    #columns = soup.find_all('div',{'curation-module__zone'}) #returns a list
    #columns = soup.find_all('div', {'class': ['curation-module__zone', 'grid__zone']})
    posts = soup.find_all('div', {'class': ['curation-module__item', 'js_curation-item box']})
   
    for i in posts:
        link =  i.find_all('a', href=True)[1]
        image_source = i.find_all('div', {'class': 'image-container'})
        
        link_text = link.text
        my_url = link['href']
        my_title = link['title']
        image_src = image_source[0].find('img')['srcset'].split()[-2]
        print(image_src)
        new_headline = Headline()
        new_headline.title = my_title
        new_headline.url = my_url
        new_headline.image = image_src
        new_headline.save()
    
    return redirect("/home/")
