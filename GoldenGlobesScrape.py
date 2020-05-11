import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

id_pattern = re.compile(r'tt\d{5,7}')

# key: film title, value: film id
ids = []

def get_search_link(string):
    words = string.split(" ")
    url1 = 'https://www.imdb.com/find?q='
    for i in range(len(words)):
        if i == 0:
            url1 += words[i]
        else:
            url1 += "+" + words[i]
    url2 = '&ref_=nv_sr_sm'
    return url1 + url2

df = pd.read_csv('data/GoldenGlobesDataRaw.csv')
films = list(df['nominee'])



for film in films:
    link = get_search_link(film)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(class_='findResult')
    id = id_pattern.findall(str(result))[0]  # find IMDB id
    ids.append(id)

id_df = pd.DataFrame(zip(films,ids), columns=['title','id'])

final_df = pd.merge(df, id_df, how='outer', left_on='nominee', right_on='title' )
final_df = final_df.set_index('id')
final_df = final_df.drop(columns=['nominee', 'ceremony'])

final_df.to_csv('data/GoldenGlobesData.csv',header=True, index_label='Const')

