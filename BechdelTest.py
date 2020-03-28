import requests
import csv
from bs4 import BeautifulSoup
import re
import pandas as pd

score_pattern = re.compile(r'[a-z]{0,2}pass.png')

data = {}
page = requests.get("https://bechdeltest.com/?list=all")
soup = BeautifulSoup(page.content, 'html.parser')
movies = soup.find_all(class_='movie')

for i,movie in enumerate(movies):
    score = score_pattern.findall(str(movie))
    title = movie.get_text().replace('\n', '').strip()
    if score[0].find('nopass') != -1:
        data[title] = False
    else:
        data[title] = True

df = pd.DataFrame.from_dict(data, orient='index', columns=['Bechdel'])
print(df.head())

df.to_csv('bechdel.csv',sep='|',header=True, index_label='Title')
