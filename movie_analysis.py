import pandas as pd
import config
import requests


#TODO- actor race, add ratings from combination of different sources, topics of the winning movies (how to determine if they were topical when released)


##globals

class MovieAnalyzer(object):

    def __init__(self):
        self.all_casts = []  # list of list of tuples (actor name, cast no) for each film
        self.all_budgets = []
        self.all_titles = []
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
        self.all_budgets.append(budget)
        self.all_titles.append(title)


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

    # def get_award(self, award_string, year):
    #     if isinstance(award_string, str):
    #         return str(year + 1) + ' Best Picture Winner'
    #     else:
    #         string = str(year + 1) + ' Best Picture Nominee'
    #         return string

    # returns 1 if film was winner of the year and  if it was nominee
    def is_oscar_award(self, award_string):
        if isinstance(award_string, str):
            return 1

        return 0
    def is_gg_award(self, win):
        if win == True or win == 'True':
            return 1
        else:
            return 0

    def make_dataframes(self):
        oscar_movies = MovieAnalyzer().get_movie_ids("data/BestPictureAcademyAward.csv")
        gg_movies = MovieAnalyzer().get_movie_ids("data/GoldenGlobesData.csv")
        movies = pd.merge(oscar_movies,gg_movies,how='outer',left_on='Const', right_on='Const')

        for Const in movies.itertuples():  # for each movie title
            movie_id = (Const[1])
            self.get_cast(movie_id)
            self.get_details(movie_id)
            self.get_keywords(movie_id)
            #print(self.all_titles)
        movies['Title'] = self.all_titles
        movies['Cast'] = self.all_casts
        movies['Budget'] = self.all_budgets
        movies['Keywords'] = self.all_keywords
        actors = pd.DataFrame(self.all_actors, columns=['Name'])
        actors['Gender'] = self.all_actor_genders

        award_info = pd.read_csv('data/BestPictureAcademyAward.csv', encoding="ISO-8859-1")
        award_info = award_info.drop(columns=['Position', 'Title', 'Created', 'Modified', 'URL', 'Title Type'])
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
        df = df[['Title', 'Cast', 'Budget', 'Keywords', 'Bechdel Pass']]

        df1 = pd.merge(df, award_info, how='left', left_index=True, right_index=True)
        final_df = pd.merge(df1, gg_award_info, how='outer', left_index=True, right_index=True)

        final_df['Year'] = final_df['Year_x'].fillna(final_df['Year_y'])
        final_df['Award Year'] = final_df['Award Year_x'].fillna(final_df['Award Year_y'])

        final_df = final_df.drop(columns=['Year_x', 'Year_y', 'Award Year_x', 'Award Year_y', 'category'])

        return final_df, actors

    
def main():
   result = MovieAnalyzer().make_dataframes()
   movies = result[0]
   actors = result[1]
   #print final dataframes
   print(movies)
   print(actors)

   movies.to_csv('data/CombinedData.csv', header=True)




if __name__ == '__main__':
    main()
