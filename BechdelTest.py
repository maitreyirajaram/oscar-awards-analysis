import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

score_pattern = re.compile(r'[a-z]{0,2}pass.png')
id_pattern = re.compile(r'tt\d{5,7}')

data = [[] for i in range (3)]
page = requests.get("https://bechdeltest.com/?list=all")
soup = BeautifulSoup(page.content, 'html.parser')
movies = soup.find_all(class_='movie')

for i,movie in enumerate(movies):
    m = str(movie)
    score = score_pattern.findall(m) # find image indicating pass or fail
    id = id_pattern.findall(m)[0] # find IMDB id
    title = movie.get_text().replace('\n', '').strip() # clean movie name string
    data[0].append(id)
    data[1].append(title)
    if score[0].find('nopass') != -1:
        data[2].append(False) # movie does not pass test
    else:
        data[2].append(True) # movie passes test

df = pd.DataFrame(list(zip(data[1],data[2])), index=data[0], columns = ['Film', 'Bechdel Pass'])

df.to_csv('data/bechdel.csv',header=True, index_label='ID')
