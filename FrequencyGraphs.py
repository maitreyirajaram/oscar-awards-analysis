import matplotlib.pyplot as plt
import altair as alt
import altair_viewer as av
import pandas as pd

# divides full movie data into two data frames, one for films that pass the bechdel test, one for those that fail
# films with no bechdel scores are not included
def split_bechdel(df):
    bechdel_pass = df[df['Bechdel Pass'] == True] # all the films that pass the Bechdel test
    bechdel_fail = df[df['Bechdel Pass'] == False] # all the films that fail the Bechdel test
    return bechdel_pass, bechdel_fail

# creates freqency graphs for genres of films that pass the bechdel test and those that don't
def bechdel_genre_graphs(bechdel_pass, bechdel_fail):
    pass_genres = []
    for row in bechdel_pass['Genres']:
        genres = row.split(", ")
        for word in genres:
            pass_genres.append(word)

    pd.Series(pass_genres).value_counts().plot(kind='bar', colormap = 'plasma', title = 'Genres of Films that Pass the Bechdel Test')
    plt.figure()


    fail_genres = []
    for row in bechdel_fail['Genres']:
        genres = row.split(", ")
        for word in genres:
            fail_genres.append(word)
    pd.Series(fail_genres).value_counts().plot(kind='bar',colormap = 'viridis', title = 'Genres of Films that Fail the Bechdel Test')
    plt.figure()
    plt.show()

# how to make altair grouped bar chart???
# group pass v fail for each genre
'''
df2 = pd.DataFrame(columns = ['Genre', 'Test'])
for i in range(len(pass_genres)):
    df2.loc[i] = [pass_genres[i], 'Pass']
for i in range(len(fail_genres)):
    df2.loc[i] = [fail_genres[i], 'Fail']

chart = alt.Chart(df2).mark_bar().encode(
    x='Test:Q',
    y='count(Genre):Q'
)
chart.show() '''
