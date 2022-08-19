from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from gensim.corpora.dictionary import Dictionary
import itertools
from collections import defaultdict
from gensim.models.tfidfmodel import TfidfModel

class NLTKprocess:
    def __init__(self,textList) -> None:
        #print(textList)
        self.preprocessed = self.preprocess(textList)
        #print(self.preprocessed)

    def preprocess(self,textList):
        articles = []
        for article in textList:
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
            articles.append(lemmatized)
        return articles

    def bow(self):
        articles = self.preprocessed
        #print(articles)
        dictionary = Dictionary(articles)
        corpus = [dictionary.doc2bow(a) for a in articles]
        
        total_word_count = defaultdict(int)
        for word_id, word_count in itertools.chain.from_iterable(corpus):
            total_word_count[word_id] += word_count

        topBOW = []
        sorted_word_count = sorted(total_word_count.items(), key=lambda w: w[1],reverse=True)
        for word_id, word_count in sorted_word_count[:5]:
            topBOW.append(f"{dictionary.get(word_id)} {word_count}")
            #print(dictionary.get(word_id), word_count)
        #print(topBOW)
        return topBOW


    def tfidf(self):
        articles = self.preprocessed
        dictionary = Dictionary(articles)
        #print(dictionary)
        #---------------------
        corpus = [dictionary.doc2bow(a) for a in articles]
        #print(corpus[0])
        #doc = corpus[0]

        tfidf = TfidfModel(corpus)
        tfidf_weights = []
        for doc in corpus:
            tfidf_weights += tfidf[doc]


        #tfidf_weights = tfidf[doc]
        #print(tfidf_weights[:5])
        
        
        #print(tfidf_weights)

        topTFIDF = []
        sorted_tfidf_weights = sorted(tfidf_weights, key=lambda w: w[1], reverse=True)
        for term_id, weight in sorted_tfidf_weights[:5]:
            #print(dictionary.get(term_id), weight)
            topTFIDF.append(f'{dictionary.get(term_id)} {weight}')
        return topTFIDF
        

    def searchWord(self,word):
        word = str(word).lower().strip()
        articles = self.preprocessed
        # print(Counter(articles).most_common(10))
        #print(articles)
        dictionary = Dictionary(articles)
        wordid =  dictionary.token2id.get(word)
        corpus = [dictionary.doc2bow(a) for a in articles]
        #print(corpus)
        
        #print(wordid)

        total_word_count = defaultdict(int)
        for word_id, word_count in itertools.chain.from_iterable(corpus):
            total_word_count[word_id] += word_count

        #print(total_word_count)

        count_of_word = 0
        sorted_word_count = sorted(total_word_count.items(), key=lambda w: w[1],reverse=True)
        for word_id, word_count in sorted_word_count:
            if (dictionary.get(word_id) == word):
                #print('-----------------')
                count_of_word = word_count
                
                #print('-----------------')
                break
        #print(wordid)
        #print(dictionary.get(computer_id))
        result = dictionary.get(wordid)
        
        #print(count_of_word)
        if result:
            return result,count_of_word
        else:
            return '',0
            #return f'Couldn\'t find the word {word} in the entire article.'





