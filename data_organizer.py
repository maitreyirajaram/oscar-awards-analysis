import pandas as pd

movies = pd.read_csv('data/FilmData.csv')
bechdel = pd.read_csv('data/bechdel.csv')

df = pd.merge(movies,bechdel,how='left',left_on=['Const'],right_on=['ID'])
df = df.drop(columns=[ 'ID', 'Film'])
df = df.set_index('Const')
df = df[['Title', 'Cast', 'Budget', 'Keywords', 'Bechdel Pass']]
df.to_csv('data/FilmData2.csv', header=True, index_label = 'ID')