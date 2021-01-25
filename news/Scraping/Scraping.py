from pprint import pprint
import re
from bs4 import BeautifulSoup
import requests
from summarizer.algorithms.scoring import scoring_algorithm, scoring_nepali
from .yahoo_scrape import get_the_news

def bbc_scraping():
    news = get_the_news('iphone')
    # scrape_bbc_popular_stories()
    # page = requests.get("https://www.bbc.com/news")
    # soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup)
    newsDict = dict()
    # div = soup.find('div', class_="nw-c-most-read__items gel-layout gel-layout--no-flex")
    # newslist = div.find_all('div', class_="gs-o-media__body")  # find_all for all
    for n in news:
    #     news = newslist[i].a['href']
    #     news1 = 'https://www.bbc.com' + news
    #     page1 = requests.get(news1)
    #     soup1 = BeautifulSoup(page1.content, 'html.parser')
    #     heading = soup1.find('h1', class_='story-body__h1')
    #     body_div = soup1.find('div', class_='story-body__inner')
    #     print(body_div)
    #     body_paragraphs = body_div.find_all('p')
    #     body = ''
    #     for p in body_paragraphs:
    #         body = body + '\n' + p.get_text()
        result_list = scoring_algorithm.scoring_main(n['description'], 5)
        summary = ' '.join(result_list)
        # pprint(body)
        newsDict[n['link']] = summary
    return newsDict


def cnn_scraping():
    page = requests.get("http://rss.cnn.com/rss/edition.rss")
    soup = BeautifulSoup(page.content,'lxml')
    
    items = soup.find_all('li')
    newsDict = dict()
    titles = []
    links = []
    for i in items[:1]:
        # print(i)
        titles.append(i.title.get_text())
        links.append(i.get_text())
    print('########## Titles ############')
    print(titles)

    print('\n\n')
    print('########## Links ############')
    print(links)


    
    for count, l in enumerate(links):
        link = l.split(',')[0]
        print(link)
        # print(l)
        page1 = requests.get(link)
        soup1 = BeautifulSoup(page1.content, 'html.parser')
        pg = ''
        if re.match(r'^https://money.cnn', l) is not None:
            body_div_m = soup1.find('div', class_='storytext')
            body_p = body_div_m.find_all('p')
            print(body_p)
            for p in body_p:
                pg = pg + '\n' + p.get_text()
        else:
            body_div = soup1.find_all('div', class_='zn-body__paragraph')
            for div in body_div:
                pg = pg + '\n' + div.get_text()
        print(pg)
        # getting summary 
        result_list = scoring_algorithm.scoring_main(pg, 5)
        summary = ' '.join(result_list)
        newsDict[titles[count]] = summary
    print(newsDict)
    return newsDict


def nagarik_scraping():
    page = requests.get("https://nagariknews.nagariknetwork.com/")
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find('div', class_="col-sm-4 title-second")
    links = div.find_all('a', class_=lambda x: x != "heading-link")
    newsDict = dict()
    titles = []
    body_links = []
    for i in range(5):
        titles.append(links[i].get_text())
        body_links.append('https://nagariknews.nagariknetwork.com' + links[i].get('href'))

    for count, l in enumerate(body_links):
        page1 = requests.get(l)
        soup1 = BeautifulSoup(page1.content, 'html.parser')
        div1 = soup1.find(id="newsContent")
        pgs = div1.find_all('p')
        body = ''
        for p in pgs:
            body = body + '\n\n' + p.get_text()
        result_list = scoring_nepali.scoring_main(body, 5)
        summary = ' '.join(result_list)
        newsDict[titles[count]] = summary
    return newsDict
