from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ovebhjrypormqo:bfa8795629ebd03539db0bb4dd2596228027f9ff3362ac69c59ad3fd8707b97c@ec2-54-164-241-193.compute-1.amazonaws.com:5432/d6ouiees3s60o0'
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


#This is the index route where we are going to
#query on all the memes
@app.route('/', methods = ['GET'])
def Index():
    all_data = Data.query[:-101:-1]

    return render_template("index.html", memes = all_data)
    #return jsonify(all_data)


#This route is for inserting data to database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        caption = request.form['caption']
        url = request.form['url']


        my_data = Data(name, caption, url)
        exists = db.session.query(Data.id).filter_by(name=name, caption=caption, url=url).scalar() is not None
        if not exists:
            db.session.add(my_data)
            db.session.commit()
            flash("Added Successfully!")
        else:
            flash("Duplicate!")
        

        return redirect(url_for('Index'))
        #return jsonify(my_data)

#This is the update route where we are going to update a meme
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.caption = request.form['caption']
        my_data.url = request.form['url']
    
        db.session.commit()
        flash("Updated Successfully!")

        return redirect(url_for('Index'))
        #return jsonify(my_data)




#This route is for deleting a meme
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Deleted Successfully!")

    return redirect(url_for('Index'))
    #all_data = Data.query.all()
    #return jsonify(all_data)
    






if __name__ == "__main__":
    app.run(debug=True)


