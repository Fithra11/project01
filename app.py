from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connection_string = 'mongodb+srv://test:sparta@cluster0.valxfy8.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string)
db = client.dbtugas9

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}))  # Mengambil semua data dari database
    response_data = []

    for article in articles:
        response_data.append({
            "title": article["title"],
            "content": article["content"],
            "file": article.get("file", "default-image.jpg")
        })

    return jsonify({"articles": response_data})

@app.route('/diary', methods=['POST'])
def save_diary():
    #sample_receive = request.form['sample_give']
    #print(sample_receive)
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}.{extension}'
    file.save(filename)

    doc = {
    'file': filename,
    'title': title_receive,
    'content': content_receive
    }
    db.diary.insert_one(doc)
    return jsonify({'msg': 'POST request complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)