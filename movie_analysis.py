import logging

import pandas as pd
from requests import HTTPError

import config
import requests
from rotten_tomatoes_client import RottenTomatoesClient


#TODO-



class MovieAnalyzer(object):

    def __init__(self):
        self.all_casts = []  # list of list of tuples (actor name, cast no) for each film
        self.all_budgets = []
        self.all_titles = []
        self.all_genres = []
        self.all_release_dates = []
        self.all_runtimes = []
        self.all_reviews = []
        self.all_keywords = []  # list of list of keywords for each film
        self.all_actors = []  # list of names
        # FULL CAST/GENDERS FOR EACH: 2 - guy, 1 - girl, ignore 0s (unfortunately makes for small margin of error)
        self.all_actor_genders = []  # list of genders (added in order)


    def get_movie_ids(self, filename):
        df = pd.read_csv(filename, usecols = ["Const"])
        return df

    def get_details(self, movie_id):
        call ='https://api.themoviedb.org/3/movie/' + str(movie_id) + '?api_key=' + config.MY_KEY + '&language=en-US'
        r = requests.get(call)
        budget = r.json().get('budget')
        title = r.json().get('original_title')
        runtime = r.json().get('runtime')
        rel_date = r.json().get('release_date')
        genres = r.json().get('genres')
        film_genres = []
        if genres is None:
            film_genres = []
        else:
            for pair in genres:
                film_genres.append(pair['name'])

        self.all_genres.append(film_genres)
        self.all_budgets.append(budget)
        self.all_titles.append(title)
        self.all_release_dates.append(rel_date)
        self.all_runtimes.append(runtime)
        return title, rel_date

    def split_year(self, release_date):
        if release_date is None:
            return -1
        delims = "-"
        year = release_date.split(delims)[0]
        year = int(year)
        return year

    def get_cast(self, movie_id):
        call = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + '/credits?api_key=' + config.MY_KEY
        r = requests.get(call)
        cast = r.json().get('cast')
        # iterate through cast
        cast_for_movie = []
        if cast is not None:
            for item in cast:
                actor_name = item.get('name')
                cast_for_movie.append((actor_name, item.get('cast_id')))  # adding cast[(actor_name, rank_of_appearance)]
                if actor_name not in self.all_actors:
                    self.all_actors.append(actor_name)
                    self.all_actor_genders.append(item.get('gender')) #add actor name and gender to list
        self.all_casts.append(cast_for_movie)

    def get_keywords(self, movie_id):
        call = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + '/keywords?api_key=' + config.MY_KEY
        r = requests.get(call)
        keywords = r.json().get('keywords')
        movie_keywords = []
        if keywords is not None:
            for item in keywords:
                word = item.get('name')
                movie_keywords.append(word) # add all keywords for this film
        self.all_keywords.append(movie_keywords)


    # returns 1 if film was winner of the year and 0 if it was nominee
    def is_oscar_award(self, award_string):
        if isinstance(award_string, str):
            return 1
        return 0

    def is_gg_award(self, win):
        if win == True or win == 'True':
            return 1
        else:
            return 0

    def is_Int(self, value): ##for review
        try:
            int(value)
            return value
        except:
            return -1


    def get_review(self, movie_title: str, year) -> None:
        tomato_meter = -1
        try:
            result = RottenTomatoesClient.search(term=movie_title)

            for item in result.get('movies'):
                if item.get('name') == movie_title:  #some movies do not have release date
                    if item.get('year') == year:
                        tomato_meter = self.is_Int(item.get('meterScore'))
        except HTTPError as ex:
            logging.exception(ex)
        self.all_reviews.append(tomato_meter)

    def make_dataframes(self):
        logging.info("Starting ...")
        oscar_movies = MovieAnalyzer().get_movie_ids("data/BestPictureAcademyAward.csv")
        gg_movies = MovieAnalyzer().get_movie_ids("data/GoldenGlobesData.csv")
        movies = pd.merge(oscar_movies,gg_movies,how='outer',left_on='Const', right_on='Const')
        logging.info("Getting cast, details, reviews etc ...")
        count = 0
        for Const in movies.itertuples():  # for each movie title
            count += 1
            movie_id = (Const[1])
            self.get_cast(movie_id)
            result = self.get_details(movie_id)
            self.get_keywords(movie_id)
            year = self.split_year(result[1])
            logging.info("Count {0} Movie:{1}".format(count, result[0]))
            self.get_review(result[0], year)
            #print(self.all_titles)
        movies['Title'] = self.all_titles
        movies['Cast'] = self.all_casts
        movies['Budget'] = self.all_budgets
        movies['Keywords'] = self.all_keywords
        movies['Genres'] = self.all_genres
        movies['Release Date'] = self.all_release_dates
        movies['Runtime'] = self.all_runtimes
        movies['Tomatometer'] = self.all_reviews
        #change all ratings back to type int
        movies['Tomatometer'] = movies['Tomatometer'].astype('int32').values
        #movies['Tomatometer'] = self.all_reviews
        actors = pd.DataFrame(self.all_actors, columns=['Name'])
        actors['Gender'] = self.all_actor_genders

        award_info = pd.read_csv('data/BestPictureAcademyAward.csv', encoding="ISO-8859-1")
        award_info = award_info.drop(columns=['Position', 'Title', 'Created', 'Modified', 'Genres', 'URL', 'Title Type', 'Runtime (mins)', 'Release Date'])
        award_info = award_info.rename(columns={"Const": 'ID'})
        award_info = award_info.set_index('ID')
        #award_info['Award'] = award_info.apply(lambda row: self.get_award(row['Description'], row['Year']), axis=1)
        award_info['Award Year'] = award_info.apply(lambda row: row['Year'] +1, axis=1)
        award_info['Oscar Winner'] = award_info.apply(lambda  row: self.is_oscar_award(row['Description']), axis=1)
        award_info = award_info.drop(columns=['Description'])

        gg_award_info = pd.read_csv('data/GoldenGlobesData.csv')
        gg_award_info = gg_award_info.drop(columns=['film', 'title'])
        gg_award_info = gg_award_info.rename(columns={"Const": 'ID', "year_award": "Award Year", 'year_film': 'Year'})
        gg_award_info['Golden Globes Winner' ] = gg_award_info.apply(lambda row: self.is_gg_award(row['win']), axis=1)
        gg_award_info = gg_award_info.drop(columns=['win'])
        gg_award_info = gg_award_info.set_index('ID')


        bechdel = pd.read_csv('data/bechdel.csv')
        df = pd.merge(movies, bechdel, how='left', left_on=['Const'], right_on=['ID'])
        df = df.drop(columns=['ID', 'Film'])
        df = df.rename(columns={"Const": 'ID'})
        df = df.set_index('ID')
        #df = df[['Title', 'Cast', 'Budget', 'Keywords', 'Genres', 'Runtime','Release Date', 'Bechdel Pass']]

        df1 = pd.merge(df, award_info, how='left', left_index=True, right_index=True)

        final_df = pd.merge(df1, gg_award_info, how='outer', left_index=True, right_index=True)

        final_df['Year'] = final_df['Year_x'].fillna(final_df['Year_y'])
        final_df['Award Year'] = final_df['Award Year_x'].fillna(final_df['Award Year_y'])

        final_df = final_df.drop(columns=['Year_x', 'Year_y', 'Award Year_x', 'Award Year_y', 'category'])

        return final_df, actors

    
def main():
    #logging because runtime is awful for rotten tomatoes client!
    # notes titles that fail (HTTP gateway error)--> batch and rerun
    # bash: tail -f ratings.log to track progress    ~25min.
    logging.basicConfig(filename="ratings.log", level=logging.INFO)


    result = MovieAnalyzer().make_dataframes()
    movies = result[0]
    actors = result[1]

    #write to csv
    movies.to_csv("movies.csv")
    actors.to_csv("actors.csv", index=False)

    #print final dataframes
    print(movies['Title'])
    print(movies['Tomatometer'])
    print(actors)

if __name__ == '__main__':
    main()
