from concurrent.futures import process
from contextlib import redirect_stderr
from operator import le
from sqlite3 import Time
from flask import Flask,render_template,request,jsonify,session,redirect,url_for
from flask_session import Session
from werkzeug.utils import secure_filename
# import mainurl
from process import NLTKprocess as p
import json
import pathlib
from datetime import datetime as date


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
ALLOWED_EXTENSIONS = {'txt'}


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/searchword',methods=['POST'])
def searchword():
    articles=request.json['articles']
    searchWord=request.json['search']
    
    process = p(articles)
    result,count_Bag = process.searchWord(searchWord)
    htmlList,count_Raw =  process.searchWordRaw_HTML(articles,searchWord)

    return jsonify({'message':'success','searchword':str(searchWord).lower().strip(),'searchresult':result,'count_Bag':count_Bag,'count_Raw':count_Raw,'htmlList':htmlList})


@app.route('/entlabel',methods=['POST'])
def entlabel():
    articles=request.json['articles']
    process = p(articles)
    return jsonify({'message':'success','nerList':process.spacyNER(articles)})

@app.route('/uploadertypetext',methods=['POST'])
def uploadertypetext():
    #print('test')
    Raw_articles = [request.json['text']]
    process = p(Raw_articles)
    return jsonify({'message':'success','topBOW':process.bow(),'topTFIDF':process.tfidf()})


# @app.route('/main',methods=['GET'])
# def main2():
#     print(9999)
#     return jsonify({'message': 'success'})



@app.route('/main', methods=['POST'])
def main():
    filenames = request.form.getlist('filenames')
    articles = request.form.getlist('articles')
    print(articles)
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

    

@app.route('/fakeNews',methods=['POST'])
def predicFakeNews():
    news=request.json['articles'][0]
    process = p(news)
    return jsonify({'message':'success','predic': process.predicFakeNews(news,convert_to_label=True)})

@app.route('/sentiment',methods=['POST'])
def sentiment():
    text=request.json['articles'][0]
    process=p(text)
    polarity,subjectivity = process.sentiment(text)
    return jsonify({'message':'success','polarity': polarity,'subjectivity':subjectivity})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)