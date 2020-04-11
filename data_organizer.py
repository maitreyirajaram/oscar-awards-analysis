import pandas as pd

def get_award(award_string, year):
    if isinstance(award_string,str):
            return str(year+1) + ' Best Picture Winner'
    else:
        string = str(year+1) + ' Best Picture Nominee'
        return string

movies = pd.read_csv('data/FilmData.csv')
bechdel = pd.read_csv('data/bechdel.csv')
award_info = pd.read_csv('data/BestPictureAcademyAward.csv', encoding="ISO-8859-1")

award_info = award_info.drop(columns=['Position', 'Title', 'Created','Modified','URL','Title Type'])
award_info =award_info.rename(columns={"Const": 'ID'})
award_info = award_info.set_index('ID')
award_info['Award'] = award_info.apply(lambda row: get_award(row['Description'],row['Year']),axis=1)
award_info = award_info.drop(columns =['Description'])

df = pd.merge(movies,bechdel,how='left',left_on=['Const'],right_on=['ID'])
df = df.drop(columns=[ 'ID', 'Film'])
df =df.rename(columns={"Const": 'ID'})
df = df.set_index('ID')
df = df[['Title', 'Cast', 'Budget', 'Keywords', 'Bechdel Pass']]
final_df = pd.merge(df, award_info, how='left', left_index=True, right_index=True)

final_df.to_csv('data/FilmData2.csv', header=True, index_label = 'ID')