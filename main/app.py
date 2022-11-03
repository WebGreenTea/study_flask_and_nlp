from flask import Flask,render_template,request,jsonify
# import mainurl
from process import NLTKprocess
import pathlib
from datetime import datetime as date

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt'}
process = NLTKprocess()

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/searchword',methods=['POST'])
def searchword():
    articles=request.json['articles']
    searchWord=request.json['search']
    result,count_Bag = process.searchWord(searchWord,articles)
    htmlList,count_Raw =  process.searchWordRaw_HTML(articles,searchWord)

    return jsonify({'message':'success','searchword':str(searchWord).lower().strip(),'searchresult':result,'count_Bag':count_Bag,'count_Raw':count_Raw,'htmlList':htmlList})


@app.route('/entlabel',methods=['POST'])
def entlabel():
    articles=request.json['articles']
    
    return jsonify({'message':'success','nerList':process.spacyNER(articles)})

@app.route('/uploadertypetext',methods=['POST'])
def uploadertypetext():
    #print('test')
    Raw_articles = [request.json['text']]
    
    return jsonify({'message':'success','topBOW':process.bow(),'topTFIDF':process.tfidf()})


@app.route('/main', methods=['POST'])
def main():
    filenames = request.form.getlist('filenames')
    articles = request.form.getlist('articles')
    #save file
    currentTime = str(date.now()).replace('.','_').replace(':','-')
    if(len(filenames) == len(articles)):
        i = 0
        for filename in filenames:
            fileName_toSave = currentTime+'_'+filename
            path = f"{str(pathlib.Path(__file__).parent.resolve().as_posix())}/text_files/{fileName_toSave}"
            file = open(path, 'w',encoding="utf-8")
            file.write(articles[i])
            file.close()
            i+=1
    data = {'filenames':filenames,'articles':articles}
    return render_template('main.html', data=data)

@app.route('/tfidf',methods=['POST'])
def tfidf():
    articles=request.json['articles']
    try:
        top = request.json['top']
    except:
        top = None
    
    word,tf_idf = process.tfidf(articles,top)
    return jsonify({'message':"success",'word':word,'tfidf':tf_idf})
    

@app.route('/bag',methods=['POST'])
def bag():
    articles=request.json['articles']
    try:
        top = request.json['top']
    except:
        top = None
    
    word,quantity = process.bow(articles,top)
    return jsonify({'message':'success','word': word,'quantity':quantity})

@app.route('/fakeNews',methods=['POST'])
def predicFakeNews():
    articles=request.json['articles']
    
    return jsonify({'message':'success','predic': process.predicFakeNews(articles)})

@app.route('/sentiment',methods=['POST'])
def sentiment():
    articles=request.json['articles']
    polarity,subjectivity = process.sentiment(articles)
    return jsonify({'message':'success','polarity': polarity,'subjectivity':subjectivity})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)