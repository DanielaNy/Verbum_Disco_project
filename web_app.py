from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from random import randint, random, choice
import os

from wtforms import Form, BooleanField, StringField, SubmitField, PasswordField, HiddenField, validators       # to be checked
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "supersecretkey"                 # wtforms need it
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
bootstrap = Bootstrap(app)

import game
db = SQLAlchemy(app)

@app.route("/")
def index():
    img_root = os.path.join(APP_ROOT, "static/images/index/")
    print(img_root, "img root")
    random_image = choice([x for x in os.listdir(img_root)
                    if os.path.isfile(os.path.join(img_root, x))])
    print(random_image, "random image")
    return render_template("index.html", random_image=random_image, img_root=img_root)

@app.route("/how_to/")
def how_to():
    return render_template("how_to.html",no_of_selected=game.no_of_selected)

@app.route("/exampletxt/")
def exampletxt():
    return render_template("exampletxt.html")

@app.route("/game/")
def game_web():    
    return render_template("game.html")

@app.route("/upload/")
def upload():
    return render_template("upload.html")

@app.route("/upload_completed/", methods=['POST'])
def upload_complete():
    """"""
    game.save_uploaded_file()

    return render_template("upload_completed.html")   

@app.route("/play/", methods=['GET'])
def play():
    chosen_list = game.prepare_game()
    
    class TranslationForm(FlaskForm):
        word1 = StringField(chosen_list[0][0])
        word2 = StringField(chosen_list[1][0])
        word3 = StringField(chosen_list[2][0])
        word4 = StringField(chosen_list[3][0])
        word5 = StringField(chosen_list[4][0])
        word_ids = HiddenField()
        submit = SubmitField('Submit')

    chosen_word_ids = ','.join(str(word[2]) for word in chosen_list)
    form = TranslationForm(word_ids= chosen_word_ids)

    return render_template("play.html", chosen_list=chosen_list, form=form)


@app.route('/result/', methods = ['POST'])
def result():
    points = 0
    form_words = [request.form["word1"], request.form["word2"], request.form["word3"], request.form["word4"], request.form["word5"]]
    word_ids = request.form["word_ids"].split(",")
    final_list = game.evaluate_game(form_words, word_ids)
    for final in final_list: 
        if final[3] == True: points += 1
    print("Final_list:", final_list)
    return render_template("result.html", final_list=final_list, points=points)

     
@app.route('/end/')
def end():
    game.end_game()
    return render_template("end.html")

if __name__ == "__main__":
    app.run()
    # app.run(host="0.0.0.0", port="5000")
    
