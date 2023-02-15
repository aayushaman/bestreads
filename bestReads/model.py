import numpy as np
import pandas as pd
from fastai.vision.all import *
from sklearn.metrics.pairwise import cosine_similarity  


#Importing the dataset
books = pd.read_csv('../dataset/Books.csv',low_memory=False)
ratings = pd.read_csv('../dataset/Ratings.csv',low_memory=False)
users = pd.read_csv('../dataset/Users.csv',low_memory=False)

#Popularity based recommendation system


ratings_with_name = ratings.merge(books, on='ISBN')
num_ratings_df = ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_ratings_df.rename(columns={'Book-Rating':'Ratings'}, inplace=True)

avg_ratings_df = ratings_with_name.groupby('Book-Title')['Book-Rating'].mean().reset_index()
avg_ratings_df.rename(columns={'Book-Rating':'Average Ratings'}, inplace=True)


popularity_df = num_ratings_df.merge(avg_ratings_df, on='Book-Title')

popular_df = popularity_df[popularity_df['Ratings'] >= 250].sort_values('Average Ratings', ascending=False).head(100)

popular_books = popular_df.merge(books, on='Book-Title').drop_duplicates('Book-Title')[['Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Ratings', 'Average Ratings', 'Image-URL-M']]



#Collaborative Filtering based recommendation system


valid_users = ratings_with_name.groupby('User-ID').count()['Book-Rating'] >= 200

literate_users = valid_users[valid_users].index

#Filtered ratings based on Users who have rated atleast 200 books
filtered_ratings = ratings_with_name[ratings_with_name['User-ID'].isin(literate_users)]


valid_books = filtered_ratings.groupby('Book-Title').count()['Book-Rating'] >= 50

famous_books = valid_books[valid_books].index

final_ratings = filtered_ratings[filtered_ratings['Book-Title'].isin(famous_books)]

pt = final_ratings.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating').fillna(0)

similarity_score = cosine_similarity(pt)
