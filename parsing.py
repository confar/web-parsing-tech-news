import os
import requests
from bs4 import BeautifulSoup
from numpy import nan as NaN
import pandas as pd


path = r'PATH_TO_YOUR_DIR_HERE'

# vc.ru parsing
r1 = requests.get('https://vc.ru/')
soup = BeautifulSoup(r1.text, 'html.parser')

resultsvc = soup.find_all('div', 'feed__item')
recordsvc = []
for result in resultsvc:
    author = result.find('span', 'entry_header__author__name')
    if author is not None:
        author = result.find('span', 'entry_header__author__name').text.strip()
    title = result.find('h2').text.strip()
    desc = result.find('p').text.strip()
    link = result.find('a')['href']
    upvote = result.find(
        'span', 'vote__value__v vote__value__v--virtual vote__value__v--current')
    if upvote is not None:
        upvote = result.find(
            'span', 'vote__value__v vote__value__v--virtual vote__value__v--current').text
    recordsvc.append((author, title, desc, link, upvote))

# mashable parsing
r2 = requests.get('http://mashable.com/tech/')
soup = BeautifulSoup(r2.text, 'html.parser')

resultsmash = soup.find_all('article')
recordsmash = []
for result in resultsmash:
    title = result.find('h1').text
    link = result.find('a')['href']
    recordsmash.append((title, link))

# techrunch
r3 = requests.get('https://techcrunch.com/startups/')
soup = BeautifulSoup(r3.text, 'html.parser')

resultstech = soup.find_all('div', 'block-content',)
recordstech = []
for result in resultstech:
    title = result.find('h2').text.strip()
    desc = result.find('p', 'excerpt').text.strip()
    link = result.find('a')['href']
    recordstech.append((title, desc, link))

# concatenating dataframes in pandas
dfvc = pd.DataFrame(recordsvc, columns=[
                    'author', 'title', 'desc', 'link', 'upvote'])
empty_row1 = pd.Series([NaN, NaN, NaN, NaN, NaN], index=[
                       'author', 'title', 'desc', 'link', 'upvote'])
dfvc_empty_row = dfvc.append(empty_row1, ignore_index=True)

dfmash = pd.DataFrame(recordsmash, columns=['title', 'link'])
empty_row2 = pd.Series([NaN, NaN], index=['title', 'link'])
dfmash_empty_row = dfmash.append(empty_row2, ignore_index=True)

dftech = pd.DataFrame(recordstech, columns=['title', 'desc', 'link'])
empty_row3 = pd.Series([NaN, NaN, NaN], index=['title', 'desc', 'link'])
dftech_empty_row = dftech.append(empty_row3, ignore_index=True)

frames = [dfvc_empty_row, dfmash_empty_row, dftech_empty_row]
results = pd.concat(frames)

results.to_csv(os.path.join(path, r'parsing.csv'),
               index=False, encoding='utf-8')
