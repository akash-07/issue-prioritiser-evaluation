import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import pickle
from gensim import corpora, models
from pprint import pprint
from sklearn.metrics import accuracy_score
import nltk

nltk.download('wordnet')

def lemmatize_stemming(text):
    stemmer = SnowballStemmer('english')
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    for token in simple_preprocess(text):
        if token not in STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

f = open('data/tf_closed_issues.pickle', 'rb')
issues = pickle.load(f)
f.close()

docs = []
labels = []
p_docs = []
for issue in issues:
    if issue['labels'] == []:
        continue
    labels.append(issue['labels'])
    text = ''
    if issue['title'] is not None:
        text += issue['title']

    # Uncomment if you want to include issue body

    # text += ' '
    # if issue['body'] is not None:
    #     text += issue['body']
    
    words = []
    docs.append(text)
    p_docs.append(preprocess(text))

print('Number of documents with labels:', len(p_docs))

processed_labels = []
for label in labels:
    label_string = ''
    for l in label:
        label_string += l['name']
    processed_labels.append(label_string)

dictionary = gensim.corpora.Dictionary(p_docs)
dictionary.filter_extremes(no_below = 50, no_above = 0.6, keep_n = 100000)

bow_corpus = [dictionary.doc2bow(doc) for doc in p_docs]

tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]

lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics = 3, \
    id2word = dictionary, passes = 2, workers = 4)

for idx, topic in lda_model_tfidf.print_topics(-1, num_words=5):
    print('Topic: {} \nWords: {}'.format(idx, topic))

# Print identified topics for some samples
for i in range(20, 22):
    print('\n---')
    print(docs[i], '\n')
    print(labels[i], '\n')
    for index, score in lda_model_tfidf[corpus_tfidf[i]]:
        print('\n Score: {}\nTopic: {}'.format(score, \
            lda_model_tfidf.print_topic(index, 5)))