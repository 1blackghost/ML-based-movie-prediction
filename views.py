from flask import jsonify, request, session
from main import app
from Prediction import predict
from Scraper import imdb_scraper
from collections import Counter
from DBMS import helper
import threading
import random


def create_new_thread(movie_name, uid):
    movie_id = imdb_scraper.get_movie_id(movie_name)
    generated = random.randint(1, 23)
    helper.update_user(uid, progress=generated, message="Connected To IMDb")

    reviews_data = imdb_scraper.get_movie_reviews(movie_id, num_reviews=200, augmentation_factor=2)
    generated = random.randint(28, 49)
    helper.update_user(uid, progress=generated, message="Analyzing Reviews")
    print(reviews_data)
    reviews, sentiments = zip(*reviews_data)
    sentiment_counts = Counter(sentiments)
    generated = random.randint(55, 73)
    helper.update_user(uid, progress=generated)
    print(sentiment_counts[1], sentiment_counts[0])
    data, accuracy = predict.predict_movie(reviews_data)

    if data:
        helper.update_user(uid, progress=100, message="Completed",sentiment="Positive:"+str(accuracy))
    else:
        helper.update_user(uid, progress=100, message="Completed",sentiment="Negative:"+str(accuracy))



@app.route("/getMovie", methods=["POST", "GET"])
def get_movie():
    name = request.form.get("movieName")
    session["uid"] = helper.insert_user(movie_name=name, progress=0, message="Fetching Movie Id")
    t = threading.Thread(target=create_new_thread, args=(name, session["uid"]))
    t.start()
    return {"status": "ok", "message": "fetching movie id"}


@app.route("/ping", methods=["GET", "POST"])
def ping():
    data = helper.read_user(session["uid"])
    print(data)
    if data[2]==100:
        data=str(data[4]).split(":")
        return {"status":"ok","percentage":100,"sentiment":data[0],"accuracy":data[1]}
    return {"status": "ok", "percentage": data[2], "message": data[3]}
