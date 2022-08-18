from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from gensim.corpora.dictionary import Dictionary
import itertools
from collections import defaultdict
from gensim.models.tfidfmodel import TfidfModel
articles = []
txt = ['Netflix can be accessed via web browsers or via application software installed on smart TVs,','']
#preprocess
for f in txt :
    
    
    article = f
    # Tokenize the article: tokens
    tokens = word_tokenize(article)
    # Convert the tokens into lowercase: lower_tokens
    lower_tokens = [t.lower() for t in tokens]
    # Retain alphabetic words: alpha_only
    alpha_only = [t for t in lower_tokens if t.isalpha()]
    # Remove all stop words: no_stops
    no_stops = [t for t in alpha_only if t not in stopwords.words('english')]
    # Instantiate the WordNetLemmatizer
    wordnet_lemmatizer = WordNetLemmatizer()
    # Lemmatize all tokens into a new list: lemmatized
    lemmatized = [wordnet_lemmatizer.lemmatize(t) for t in no_stops]
    #list_article
    articles.append(lemmatized)


#print(articles[0])
#---------------------

#สร้าง dictionary มี id คู่กับคำ
dictionary = Dictionary(articles)
#print(dictionary)
#---------------------
corpus = [dictionary.doc2bow(a) for a in articles]
#print(corpus[0])
doc = corpus[0]
print(corpus)
tfidf = TfidfModel(corpus)
tfidf_weights = tfidf[doc]
#print(tfidf_weights[:5])

sorted_tfidf_weights = sorted(tfidf_weights, key=lambda w: w[1], reverse=True)
for term_id, weight in sorted_tfidf_weights[:5]:
    print(dictionary.get(term_id), weight)