from operator import le
from flask import Flask,render_template,request,redirect,url_for,flash,session,jsonify
from flask_session import Session
from werkzeug.utils import secure_filename
import os
import mainurl
from process import NLTKprocess as p
import json

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



ALLOWED_EXTENSIONS = {'txt'}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result")
def result():
    topBOW = session.get('topBOW')
    topTFIDF = session.get('topTFIDF')
    Raw_articles = session.get('Raw_articles')
    return render_template("result.html",topBOW = topBOW, topTFIDF = topTFIDF,Raw_articles=Raw_articles) 
    #return render_template("result.html")    


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file[]' not in request.files:
            #flash('No file part')
            return redirect(mainurl.MAIN_URL)
        
        files = request.files.getlist("file[]")
        
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        
        Raw_articles = []
        for file in files:
            if file.filename == '':
                #flash('No selected file')
                return redirect(mainurl.MAIN_URL)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(f"text_files/{filename}"))
                
                f = open(f"./text_files/{filename}", "r")
                Raw_articles.append(f.read())
                #print(p.preprocessed)
                #return render_template("result.html",topBOW=topBOW)
            else:
                return redirect(mainurl.MAIN_URL)
        
        process = p(Raw_articles)
        
        session['topBOW'] = process.bow()
        session['topTFIDF'] = process.tfidf()
        session['Raw_articles'] = Raw_articles
        #tfidf.append(process.tfidf())
        #data = json.dumps({"topBOW":topBOW})
        return redirect(url_for('result'))
    return redirect(mainurl.MAIN_URL)


@app.route('/test', methods=['POST'])
def test():
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
            file.save(os.path.join(f"text_files/{filename}"))
            
            f = open(f"./text_files/{filename}", "r")
            Raw_articles.append(f.read())
            #print(p.preprocessed)
            #return render_template("result.html",topBOW=topBOW)
        else:
            resp = jsonify({'message': 'Invalid file'})
            resp.status_code = 400
            return resp
    process = p(Raw_articles)
    #session['topBOW'] = process.bow()
    #session['topTFIDF'] = process.tfidf()
    return jsonify({'message':'success','topBOW':process.bow(),'topTFIDF':process.tfidf()})
    # text = request.args.get('data')
    # print((text))
    # return jsonify({'testdata':text})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)