'''
This script contains the views/routes of the website

'''

from flask import jsonify,request,session
from main import app
from Prediction import predict
from Scraper import imdb_scraper
from collections import Counter

#this
movie_name = "guardians of galaxy vol 3"
movie_id = imdb_scraper.get_movie_id(movie_name)

reviews_data = imdb_scraper.get_movie_reviews(movie_id, num_reviews=200, augmentation_factor=2)
print(reviews_data)
reviews, sentiments = zip(*reviews_data)
sentiment_counts = Counter(sentiments)
print(sentiment_counts[1],sentiment_counts[0])


data,accuracy=predict.predict_movie(reviews_data)
if data:
	print("postive",accuracy)
else:
	print("negative",accuracy)