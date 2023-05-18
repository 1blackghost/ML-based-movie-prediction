from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from collections import Counter
import numpy as np
from scipy.sparse import hstack
from collections import Counter



def predict_movie(reviews_data):
    reviews, sentiments = zip(*reviews_data)
    sentiment_counts = Counter(sentiments)

    positive_reviews_count = sentiment_counts[1]
    negative_reviews_count = sentiment_counts[0]
    reviews_ratio = positive_reviews_count / negative_reviews_count

    reviews_ratio_feature = [str(reviews_ratio)] * len(reviews)

    vectorizer = TfidfVectorizer()
    X_reviews = vectorizer.fit_transform(reviews)
    X_reviews_ratio = vectorizer.transform(reviews_ratio_feature)

    if X_reviews.shape[1] < X_reviews_ratio.shape[1]:
        X_reviews = hstack([X_reviews, np.zeros((X_reviews.shape[0], X_reviews_ratio.shape[1] - X_reviews.shape[1]))])
    elif X_reviews.shape[1] > X_reviews_ratio.shape[1]:
        X_reviews_ratio = hstack([X_reviews_ratio, np.zeros((X_reviews_ratio.shape[0], X_reviews.shape[1] - X_reviews_ratio.shape[1]))])

    X_combined = hstack((X_reviews, X_reviews_ratio))

    X_train, X_test, y_train, y_test = train_test_split(X_combined, sentiments, test_size=0.2, random_state=42)

    mlp_classifier = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500)
    mlp_classifier.fit(X_train, y_train)

    accuracy = mlp_classifier.score(X_test, y_test)

    new_review = "This film was amazing. The performances were outstanding and the story was gripping."

    new_review_vector = vectorizer.transform([new_review])

    if new_review_vector.shape[1] < X_combined.shape[1]:
        new_review_vector = hstack([new_review_vector, np.zeros((new_review_vector.shape[0], X_combined.shape[1] - new_review_vector.shape[1]))])

    prediction = mlp_classifier.predict(new_review_vector)

    if prediction[0] == 1:
        return True,accuracy*100
    else:
        return False,accuracy*100