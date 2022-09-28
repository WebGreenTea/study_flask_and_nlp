from operator import le
from flask import Flask,render_template,request,jsonify
from werkzeug.utils import secure_filename
# import mainurl
from process import NLTKprocess as p

import pathlib

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt'}


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/searchword',methods=['POST'])
def searchword():
    articles=request.json['articles']
    searchWord=request.json['search']
    # print(len(articles))
    #print(articles)
    process = p(articles)
    result,count = process.searchWord(searchWord)

    return jsonify({'message':'success','searchword':str(searchWord).lower().strip(),'searchresult':result,'count':count})


@app.route('/entlabel',methods=['POST'])
def entlabel():
    articles=request.json['articles']
    process = p(articles)
    return jsonify({'message':'success','nerList':process.spacyNER(articles)})

@app.route('/uploadertypetext',methods=['POST'])
def uploadertypetext():
    print('test')
    Raw_articles = [request.json['text']]
    process = p(Raw_articles)
    return jsonify({'message':'success','topBOW':process.bow(),'topTFIDF':process.tfidf()})


@app.route('/uploader', methods=['POST'])
def uploader():
    if 'file[]' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist("file[]")
    Raw_articles = []
    for file in files:
        if file.filename == '':
            resp = jsonify({'message': 'No selected fil'})
            resp.status_code = 400
            return resp
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(f"text_files/{filename}"))
            path = f"{str(pathlib.Path(__file__).parent.resolve().as_posix())}/text_files/{filename}"
            file.save(path)
            print(path)
            #print((os.path.join(f"text_files/{filename}")))
            #f = open(os.path.join(f"text_files/{filename}"), "r")
            f = open(path, "r")
            Raw_articles.append(f.read())
            #print(p.preprocessed)
            #return render_template("result.html",topBOW=topBOW)
        else:
            resp = jsonify({'message': 'Invalid file'})
            resp.status_code = 400
            return resp
    process = p(Raw_articles)
    return jsonify({'message':'success','topBOW':process.bow(),'topTFIDF':process.tfidf()})

@app.route('/fakeNews',methods=['POST'])
def predicFakeNews():
    news=request.json['articles'][0]
    process = p(news)
    return jsonify({'message':'success','predic': process.predicFakeNews(news,convert_to_label=True)})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)