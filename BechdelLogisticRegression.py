import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Drama', 'Family',
          'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction',
          'Thriller', 'War', 'Western']

def process_training_data(df):
    bechdel_films = df[df['Bechdel Pass'] is True | df['Bechdel Pass'] is False]
    # first 17 entries are 0/1 indicators of genre, 18th entry is number of female cast members, 19th is number of top rank females
    training_input = np.ndarray(shape=(len(bechdel_films.index), 19))
    training_output = np.zeros(shape=len(bechdel_films))
    i = 0
    for row in bechdel_films.iterrows():
        # set output value
        score = row[1]['Bechdel Pass']
        if score is True:
            training_output[i] = 1

        # set input genre features
        genres = row[1]['Genre']
        for g in genres:
            index = genres.index(g)
            training_input[i][index] = 1

        # set input number of females
        training_input[i][17] = row[1]['no_of_females']
        training_input[i][18] = row[1]['no_of_toprank_females']

    return training_input, training_output




