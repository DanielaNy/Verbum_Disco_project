import sqlite3
import os
from random import choice, randrange
from flask import request
from flask_sqlalchemy import SQLAlchemy
from web_app import app, APP_ROOT
from sqlalchemy.exc import IntegrityError

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)

filename_txt = "user" + "_file.txt"
no_of_selected = 5
#levels = [0, 1, 2, 0, 0, 1, 0, 0, 0, 1]
chosen_list = []

class User(db.Model):                       # flask-sglalchemy z class spravi tabulku s tymto menom
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    words = db.relationship('Word', backref='user', lazy=True)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unknown = db.Column(db.String(100), unique=True, nullable=False)
    known = db.Column(db.String(100), unique=True, nullable=False)
    level = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return self.unknown, self.known

def save_uploaded_file():
    """saves the uploaded file by user into 'user' directory"""
    target = os.path.join(APP_ROOT, 'user/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = "user_file" + ".txt"
        destination = "/".join([target, filename])
        file.save(destination)

def new_words_from_text_file():
    """appends new words from the text file to the database, if user_textfile.txt uploaded"""
    db.create_all()

    def add(db):
        for line in user_file:     
            line = line.rstrip()
            uploaded_words = line.split("; ")       # list
            try:                                
                new_word = Word(unknown=uploaded_words[0], known=uploaded_words[1], level=0, user_id=1)
            except:
                IndexError
                pass
            while True:
                try:                        
                    db.session.add(new_word)
                    db.session.commit()
                    print("added new word:", new_word.unknown, new_word.known)                          # to check
                    break
                except IntegrityError:
                    db.session().rollback()
                    already_in_db = Word.query.filter_by(unknown=new_word.unknown).first()
                    if already_in_db:
                        print(already_in_db.unknown, already_in_db.known, "deleted")                    # to check
                        db.session.delete(already_in_db)                                
                        db.session.commit()
                        continue

        return user_file

    if os.path.exists('./user/user_file.txt'):
        with open("./user/"+filename_txt) as user_file:
            user_file = add(db)
        os.remove('./user/user_file.txt')
    else:
        pass
    if len(Word.query.all()) < 5:
        with open("./sample/exampletxt.txt") as user_file:
            print("words added from sample:")            
            user_file = add(db)
    else:
        print("No new words were added to the \'Word\' table.")
        pass

# def print_all_words_from_database():
#     print("\n-------------------------- all words in table below ------------------------------")
#     all_words = Word.query.all()
#     print("This is in database:")
#     for w in all_words:
#         print(w.unknown, w.known, w.level)
#     print("-------------------------- all words in table above ------------------------------\n")
#     return all_words

def select_word_to_test():
    """slects random words from the database according to algorithm"""
    print("---selecting random words---")    
    q = db.session.query(Word)
    chosen_list.clear()
    while len(chosen_list) < 5:  
        rand = randrange(0, q.count())
        row = db.session.query(Word)[rand]
        if (row.unknown, row.known, row.id) not in chosen_list:
            chosen_list.append((row.unknown, row.known, row.id))
            continue
    print(chosen_list)
    return chosen_list

def prepare_game():
    """starts the game - creates the connection to database, imports words from text file and chooses list of words for the play"""
    new_words_from_text_file()
    #print_all_words_from_database()
    chosen_list = select_word_to_test()
    # print(chosen_list)
    return chosen_list

def evaluate_game(form_words, word_ids):
    """checks, if the data input from the user corresponds to the chosen words' translation"""
    final_list = []
    idx = 0
    for w_id in word_ids:
        orig_word = Word.query.filter_by(id=w_id).first()
        tup = orig_word.unknown, orig_word.known, form_words[idx], form_words[idx] == orig_word.known
        final_list.append(tup)
        idx +=1
    return final_list

def end_game():
    """deletes the database"""
    os.remove('./db.sqlite3')

if __name__ == "__main__":
    new_words_from_text_file()
    #print_all_words_from_database()
    chosen_list  = select_word_to_test()
