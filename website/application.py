from Student import Student
from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_pymongo import PyMongo
import sys

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Students"
app.config['MONGO_DBNAME'] = 'Students'
app.config['SECRET_KEY'] = 'filesystem'

mongo=PyMongo(app)

db = mongo.db
col = mongo.db["student"]
mongo = PyMongo(app)


class SearchForm(FlaskForm):
    student_name = StringField('Student name', validators=[DataRequired()])
    submit = SubmitField('Search')

@app.route("/")
def home():

    return render_template("home.html")

@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        student_name=request.form["name"]

        return redirect(url_for("found_it", student_name=student_name))
    else:

        return render_template('search.html', title='Search')

@app.route("/addinfo", methods=['POST', 'GET'])
def add():
    if request.method == "POST":
        name=request.form["name"]
        age=request.form["age"]
        location=request.form["address"]
        col.insert_one({'name': name, 'age': age, 'location': location})

        return redirect(url_for("table"))
    else:
        return render_template('addinfo.html')

@app.route("/delete", methods=['GET', 'DELETE'])
def delete():
    if request.method == "DELETE":
        col.deleteOne({'name': name})

        return redirect(url_for("table"))
    else:
        return render_template('delete.html')
        
@app.route("/result", methods = ['GET'])
def found_it(student_name):
    student = col.find({ text: { search: "Minh" } })
    return render_template('result.html', student)

@app.route("/table")
def table():
    persons = col.find()

    return render_template("table.html", persons=persons)

if __name__ == '__main__':
  try:
    port = int(sys.argv[1])
  except (TypeError, IndexError):
    port = 8088
  app.run(debug=True, host='0.0.0.0', port=port)
