import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

stopwords = set(STOPWORDS)
stopwords.update(['based', 'novel', 'book', 'story', 'true'])

# divides full movie data into two data frames, one for films that pass the bechdel test, one for those that fail
# films with no bechdel scores are not included
def split_bechdel(df):
    bechdel_pass = df[df['Bechdel Pass'] == True] # all the films that pass the Bechdel test
    bechdel_fail = df[df['Bechdel Pass'] == False] # all the films that fail the Bechdel test
    return bechdel_pass, bechdel_fail

# creates wordclouds of the keywords of films that pass the bechdel test and of films that don't
def bechdel_keywords_cloud(bechdel_pass, bechdel_fail):
    pass_keywords = []
    for row in bechdel_pass['Keywords']:
        row = row[1:len(row)-1].replace("'","")
        words = row.split(", ")
        for word in words:
            pass_keywords.append(word)
    pass_text = " ".join(pass_keywords)

    # generate a word cloud of keywords of all films that pass the Bechdel Test
    pass_keyword_cloud = WordCloud(stopwords=stopwords, max_font_size=40, relative_scaling=1, max_words=400, background_color="white", colormap='magma').generate(pass_text)
    plt.imshow(pass_keyword_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.figure()

    fail_keywords = []
    for row in bechdel_fail['Keywords']:
        row = row[1:len(row)-1].replace("'","")
        words = row.split(", ")
        for word in words:
            fail_keywords.append(word)
    fail_text = " ".join(fail_keywords)

    # generate a word cloud of keywords of all films that fail the Bechdel Test
    fail_keyword_cloud = WordCloud(stopwords=stopwords, max_font_size=30, max_words=400, background_color="white", relative_scaling=1).generate(fail_text)
    plt.imshow(fail_keyword_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.figure()

    plt.show()




