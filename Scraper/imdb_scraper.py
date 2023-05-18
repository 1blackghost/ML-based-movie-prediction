import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
from bs4 import BeautifulSoup
import imdb
from textblob import TextBlob


def get_user_reviews(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    reviews = []
    review_elements = soup.find_all("div", class_="review-container")

    for review_element in review_elements:
        review_text = review_element.find("div", class_="text show-more__control").text.strip()
        reviews.append(review_text)

    return reviews


def sentiment_analysis(string):
    blob = TextBlob(string)
    polarity = blob.sentiment.polarity
    threshold = 0.15

    sentiment_class = 1 if polarity >= threshold else 0

    return sentiment_class


def get_movie_id(name):
    ia = imdb.IMDb()
    search = ia.search_movie(name)[0]
    return search.movieID


def get_movie_reviews(movie_id, num_reviews=100, augmentation_factor=2):
    positive_url = f"https://www.imdb.com/title/tt{movie_id}/reviews?sort=curated&dir=desc&ratingFilter=10"
    negative_url = f"https://www.imdb.com/title/tt{movie_id}/reviews?sort=curated&dir=desc&ratingFilter=1"

    positive_reviews = get_user_reviews(positive_url)[:num_reviews]
    negative_reviews = get_user_reviews(negative_url)[:num_reviews]

    positive_sentiments = [sentiment_analysis(review) for review in positive_reviews]
    negative_sentiments = [sentiment_analysis(review) for review in negative_reviews]

    reviews = positive_reviews + negative_reviews
    sentiments = positive_sentiments + negative_sentiments

    augmented_reviews = reviews * augmentation_factor
    augmented_sentiments = sentiments * augmentation_factor

    data = list(zip(augmented_reviews, augmented_sentiments))

    return data


