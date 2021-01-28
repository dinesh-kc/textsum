import requests 
from bs4 import BeautifulSoup as bs 

from .algo import fetch_summary





def extract(url):
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    soup_tag = list(filter(lambda p: len(list(p.children)) < 2, soup.find_all(['p', 'div'], class_=None, id=None)))
    text = ' '.join(map(lambda p: p.text, soup_tag))
    if text == '':
        text = 'No Paragraphs Found!'
    text = text.replace('\xa0', ' ')
    return text



  
BASE_URL = 'https://news.google.com'
URL = "{}/topstories?hl=en-US&gl=US&ceid=US:en".format(BASE_URL)
r = requests.get(URL) 
  
soup = bs(r.content, 'html5lib') 
# print(soup.prettify()) 

def convertTuple(tup): 
    str =  ''.join(tup) 
    return str
def get_google_news():
    news_boxes = soup.find_all('div',attrs={'jscontroller':'d0DtYd'})
    total_news = []

    for news_box in news_boxes:
        article = news_box.find('div',attrs={'jsname':'GNGJO'})
        link = article.find('a',attrs={'class':'DY5T1d RZIKme'})['href']
        full_link = '{}{}'.format(BASE_URL,link)   
        full_article = article.find('span',attrs={'class':'xBbh9'}).text

        time = article.find('time').text

        fa = extract(full_link)
        # print(fa)
        if len(fa) > 1:
            fa = convertTuple(fa)
            # try: 
            fs = fetch_summary(fa)
            summ = fs.load_summary(fa)
            # except:
            #     summ = "Google Doesnt allow this page"
        
            temp = {
                'link':full_link,
                'article':fa,
                'summary':summ,
                'time':time
            }
            total_news.append(temp)
    return total_news
