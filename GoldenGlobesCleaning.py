import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
def equals(x, y):
    answer = True
    if len(x) != len(y): return False

    for i in range(len(x)):
        if x[i] != y[i]:
            return False
    return answer


df = pd.read_csv('data/GoldenGlobesData.csv')
for row in df.iterrows():
    id = row[1]['Const']
    data_title = row[1]['title']
    link = 'https://www.imdb.com/title/' + id + '/?ref_=fn_al_tt_2'
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    wrapper_class = soup.find(class_='title_wrapper')
    title_class = wrapper_class.find(class_= '')
    title = str(title_class.get_text())

    if title.find('(') != -1:
        title = title[0:len(title)-8]
    title = title.strip()
    data_title = data_title.strip()
    if equals(title,data_title):
        continue
    else:
        print (id, data_title, title)



