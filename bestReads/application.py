from flask import Flask, render_template
import pickle

popular_books = pickle.load(open('popular.pkl', 'rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",
    book_name=list(popular_books['Book-Title'].values),
    book_author=list(popular_books['Book-Author'].values),
    book_year=list(popular_books['Year-Of-Publication'].values),
    book_publisher=list(popular_books['Publisher'].values),
    book_ratings=list(popular_books['Ratings'].values),
    book_image=list(popular_books['Image-URL-M'].values)
    )


if __name__ == '__main__':
    app.run(debug=True)