import pandas as pd
import config
import requests

#TODO- actor race


##globals
all_casts = [] #list of list of tuples (actor name, cast no) for each film
all_budgets = []

all_actors = [] #list of names
# FULL CAST/GENDERS FOR EACH: 2 - guy, 1 - girl, ignore 0s (unfortunately makes for small margin of error)
all_actor_genders = [] #list of genders (added in order)

def get_movie_ids(filename):
    df = pd.read_csv(filename, usecols = ["Const"])
    return df

def get_budget(movie_id):
    call ='https://api.themoviedb.org/3/movie/' + str(movie_id) + '?api_key=' + config.MY_KEY + '&language=en-US'
    r = requests.get(call)
    budget = r.json().get('budget')
    all_budgets.append(budget)

def get_cast(movie_id):
    call = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + '/credits?api_key=' + config.MY_KEY
    r = requests.get(call)
    cast = r.json().get('cast')
    # iterate through cast
    cast_for_movie = []
    for item in cast:
        actor_name = item.get('name')
        cast_for_movie.append((actor_name, item.get('cast_id')))  # adding cast[(actor_name, rank_of_appearance)]
        if actor_name not in all_actors:
            all_actors.append(actor_name)
            all_actor_genders.append(item.get('gender'))#add actor name and gender to list
    all_casts.append(cast_for_movie)

def main():
    movies = get_movie_ids("data/BestPictureAcademyAward.csv")

    for Const in movies.itertuples(): #for each movie title
        movie_id = (Const[1])
        get_cast(movie_id)
        get_budget(movie_id)
    movies['Cast'] = all_casts
    movies['Budget'] = all_budgets
    actors = pd.DataFrame(all_actors, columns=['Name'])
    actors['Gender'] = all_actor_genders

    #print final dataframes
    print(movies)
    print(actors)

if __name__ == '__main__':
    main()