import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle


def data_prep(data):
    titles_df = pd.DataFrame(data)

    # drop unnecessary columns
    titles_df.drop(
        columns=['created_at', 'creator_id', 'images', 'price', 'product_type', 'shipping_price', 'sub_category',
                 'stock', 'updated_at', 'video', 'ratings_avg', 'id'],
        axis=1, inplace=True)

    # replace NaN with empty strings
    titles_df.fillna('', inplace=True)

    titles_df['title_dup'] = titles_df['name']

    titles_corpus = titles_df.apply(' '.join, axis=1)

    tfidf_vectorizer_params = TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 3), max_df=.5)

    tfidf_vectorizer = tfidf_vectorizer_params.fit_transform(titles_corpus)
    # save model to storage
    pickle.dump(tfidf_vectorizer, open('rec_model.pickle', 'wb'))


def recommended_products(name, data, rec_model):
    data = pd.DataFrame(data)
    data = data[['name', 'id', 'images', 'price']]

    try:
        title_iloc = data.index[data['name'] == name][0]
        print("title_iloc")
        print(title_iloc)
    except Exception as e:
        return [], 'title not in dataset.'

    show_cos_sim = cosine_similarity(rec_model[title_iloc], rec_model).flatten()
    sim_titles_vects = sorted(list(enumerate(show_cos_sim)), key=lambda x: x[1], reverse=True)[1:6]

    return [{'name': data.iloc[t_vect[0]][0],
             'id': data.iloc[t_vect[0]][1],
             'images': data.iloc[t_vect[0]][2],
             'price': data.iloc[t_vect[0]][3],
             'confidence': round(t_vect[1], 1)} for t_vect in sim_titles_vects], 'recommendation successful'
