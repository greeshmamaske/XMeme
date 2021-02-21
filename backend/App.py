from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ovebhjrypormqo:bfa8795629ebd03539db0bb4dd2596228027f9ff3362ac69c59ad3fd8707b97c@ec2-54-164-241-193.compute-1.amazonaws.com:5432/d6ouiees3s60o0'
app.config['HEROKU_POSTGRESQL_BLACK_URL'] = 'postgres://uskkrhcjhbwehq:748ab8b729549d7579b7aa11994c492b9a04a9ecc80f007d00bc35c720c0782b@ec2-18-204-101-137.compute-1.amazonaws.com:5432/d45jmlgklq8rb6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["MYSQL_HOST"]="127.0.0.1"
app.config["MYSQL_USER"]="root"

db = SQLAlchemy(app)


#Creating model table for the database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    caption = db.Column(db.String(100))
    url = db.Column(db.String(5000))


    def __init__(self, name, caption, url):

        self.name = name
        self.caption = caption
        self.url = url

@app.route('/', methods = ['GET'])
def Index():
    memes = Data.query.first() 
    if memes is None:
        return("[]\n")
    memes = Data.query[:-101:-1]    
    results = [
        {
            "id": meme.id,
            "name": meme.name,
            "caption": meme.caption,
            "url": meme.url
        } for meme in memes]
    print(results)
    return jsonify(results)

#This is the index route where we are going to
#query on all the memes
@app.route('/memes', methods=['POST', 'GET'])
def handle_memes():
    #POST request to add a new meme
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_meme = Data(name=data['name'], caption=data['caption'], url=data['url'])
            exists = db.session.query(Data.id).filter_by(name=data['name'], caption=data['caption'], url=data['url']).scalar() is not None
            if not exists:
                db.session.add(new_meme)
                db.session.commit()
                return jsonify({"id":new_meme.id})
            else:
                return make_response("409: Duplicate", 409)
        else:
            return {"error": "The request payload is not in JSON format"}
    #GET request to get all the memes in database
    elif request.method == 'GET':
        memes = Data.query.first() 
    if memes is None:
        return("[]\n")
    memes = Data.query[:-101:-1]    
    results = [
        {
            "id": meme.id,
            "name": meme.name,
            "caption": meme.caption,
            "url": meme.url
        } for meme in memes]
    print(results)
    return jsonify(results)
#This route is to GET a particular id
@app.route('/memes/<id>', methods=['GET'])
def handle_memes_with_id(id):
    meme = Data.query.get(id)
    return jsonify({"id": meme.id, "name": meme.name, "caption": meme.caption, "url": meme.url})

#This route is for PATCH request to update caption/url of a meme
@app.route('/memes/<id>', methods=['PATCH'])
def update_memes_with_id(id):
    meme = Data.query.get_or_404(id)
    caption = meme.caption
    url = meme.url
    if request.is_json:
            data = request.get_json()
            if data['caption']:
                caption = data['caption']
            if data['url']:
                url = data['url']
            meme.caption = caption
            meme.url = url
            db.session.commit()
            return make_response("200", 200)

    else:
            return {"error": "The request payload is not in JSON format"}

    
                


if __name__ == "__main__":
    app.run(host="localhost", port=8081, debug=True)


