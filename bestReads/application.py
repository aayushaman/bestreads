from flask import Flask, render_template, request
import pickle, numpy as np

popular_books = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))  


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


@app.route('/recommend')
def recommend_ui():
    return render_template("recommend.html")



@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)
    similar_items = sorted(list(enumerate(similarity_score[index])), reverse=True, key=lambda x: x[1])[1:]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return render_template("recommend.html", data=data)



if __name__ == '__main__':
    app.run(debug=True)