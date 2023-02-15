from model import *
def recommedation(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), reverse=True, key=lambda x: x[1])[1:]
    for i in similar_items:
        print(pt.index[i[0]])

print(recommedation('1984'))
