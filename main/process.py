import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from gensim.corpora.dictionary import Dictionary
import itertools
from collections import defaultdict
from gensim.models.tfidfmodel import TfidfModel
import spacy
from spacy import displacy
from transformers import AutoTokenizer,AutoModelForSequenceClassification
import pathlib
from textblob import TextBlob
import re

class NLTKprocess:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        #print(textList)
        #self.preprocessed = self.preprocess(textList)
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

    def bow(self,articles,top=None):
        articles = self.preprocess(articles)
        #print(articles)
        dictionary = Dictionary(articles)
        corpus = [dictionary.doc2bow(a) for a in articles]
        
        total_word_count = defaultdict(int)
        for word_id, word_count in itertools.chain.from_iterable(corpus):
            total_word_count[word_id] += word_count

        topBOW = []
        quantity = []
        sorted_word_count = sorted(total_word_count.items(), key=lambda w: w[1],reverse=True)
        if(top):
            for word_id, word_count in sorted_word_count[:top]:
                #topBOW.append(f"{dictionary.get(word_id)} {word_count}")
                topBOW.append(dictionary.get(word_id))
                quantity.append(word_count)
                #print(dictionary.get(word_id), word_count)
        else:
            for word_id, word_count in sorted_word_count:
                topBOW.append(dictionary.get(word_id))
                quantity.append(word_count)
            
        #print(topBOW)
        return topBOW,quantity


    def tfidf(self,articles,top=None):
        articles = self.preprocess(articles)
        dictionary = Dictionary(articles)
        #print(dictionary)
        #---------------------
        corpus = [dictionary.doc2bow(a) for a in articles]
        
        
        #doc = corpus[0]

        tfidf = TfidfModel(corpus)
        tfidf_weights = []
        for doc in corpus:
            tfidf_weights += tfidf[doc]
            
        #print(f'tfidf_weights {len(tfidf_weights[1])}')
        #tfidf_weights = tfidf[doc]
        #print(tfidf_weights[:5])
        
        
        #print(tfidf_weights)

        Tfidf = []
        word = []
        sorted_tfidf_weights = sorted(tfidf_weights, key=lambda w: w[1], reverse=True)
        if(top):
            for term_id, weight in sorted_tfidf_weights[:top]:
                #print(dictionary.get(term_id), weight)
                #topTFIDF.append(f'{dictionary.get(term_id)} {weight}')
                Tfidf.append(weight)
                word.append(dictionary.get(term_id))
        else:
            for term_id, weight in sorted_tfidf_weights:
                Tfidf.append(weight)
                word.append(dictionary.get(term_id))
        return word,Tfidf
        

    def searchWord(self,word,articles):
        word = str(word).lower().strip()
        articles = self.preprocess(articles)
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
                #print(word_id)
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

    def searchWordRaw_HTML(self,articles,searchWord):
        htmlList = []
        count = 0
        searchWord = str(searchWord).lower().strip()
        for article in articles:
            match = re.findall(searchWord,article,flags=re.IGNORECASE)
            count += len(match)
            match = list(dict.fromkeys(match))
            for word in match:
                article = re.sub(word, f'<mark>{word}</mark>', article)
            htmlList.append(article)
        return htmlList,count




    def spacyNER(self,textlist):
        nlp = spacy.load('en_core_web_sm')
        # entlabelTemp = []
        # entlabel = []
        # for text in textlist:
        #     doc = nlp(text)
        #     for ent in doc.ents:
        #         if not(ent.text in entlabelTemp):
        #             entlabelTemp.append(ent.text)
        #             #print(ent.label_,ent.text)
        #             entlabel.append((ent.label_,ent.text))
        # entlabel.sort(reverse = False, key = lambda t: t[1])
        # print(entlabel)

        NERhteml = []
        for text in textlist:
            doc = nlp(text)
            NERhteml.append(displacy.render(doc, style="ent"))
        return NERhteml

    def predicFakeNews(self,articles):
        model_path = f"{str(pathlib.Path(__file__).parent.resolve().as_posix())}/model/fake-news-bert-base-uncased"
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        result = []
        # executing argmax function to get the candidate label
        d = {
            0: "reliable",
            1: "fake"
        }

        for news in articles:
            # prepare our text into tokenized sequence
            inputs = tokenizer(news, padding=True, truncation=True, max_length=512,return_tensors="pt")
            # perform inference to our model
            outputs = model(**inputs)
            # get output probabilities by doing softmax
            probs = outputs[0].softmax(1)
            result.append(d[int(probs.argmax())])
        return result
        # if convert_to_label:
        #     return 
        # else:
        #     return int(probs.argmax())

    def sentiment(self,articles):
        polarityList = []
        subjectivityList = []
        for text in articles:
            blob = TextBlob(text)
            polarity,subjectivity = blob.sentiment
            polarityList.append(polarity)
            subjectivityList.append(subjectivity)
        return polarityList,subjectivityList
                    
