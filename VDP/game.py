import sqlite3
import os
from random import choice, randrange
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, OperationalError

from VDP import app, APP_ROOT, db, logger
import VDP.models
from VDP.config_file import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from VDP.config_file import db_name, file_txt, sample_txt, no_of_selected, project_dir
from VDP.config_file import user_destination, file_in_user_destination
from VDP.config_file import sample_destination, file_in_sample_destination

chosen_list = []


def save_uploaded_file():
    """saves the uploaded file by user into 'user' directory"""
    logger.warn(f"""LOGGER WARN / file will be saved in:
        {user_destination}""")       # to check
    if not os.path.isdir(user_destination):
        os.mkdir(user_destination)
        logger.warn(f"LOGGER WARN /{user_destination} created")      # to check

    for file in request.files.getlist("file"):
        logger.warn(f"LOGGER WARN / file saved as: {file_txt}")      # to check
        file.save(file_in_user_destination)


def _add(db, user_file):
    for line in user_file:
        line = line.rstrip()
        uploaded_words_from_one_line = line.split("; ")    # list
        try:
            new_word = VDP.models.Word(
                unknown=uploaded_words_from_one_line[0],
                known=uploaded_words_from_one_line[1],
                level=0,
                user_id=1)
        except IndexError:
            logger.warn(
                f"""LOGGER WARN / error while processing item:
                {line}""")  # to check
        while True:
            try:
                db.session.add(new_word)
                db.session.commit()
                logger.warn(
                    f"""LOGGER WARN / added new word:{new_word.unknown},
                    {new_word.known}""")  # to check
                break
            except IntegrityError:
                db.session().rollback()
                already_in_db = VDP.models.Word.query.filter_by(
                    unknown=new_word.unknown).first()
                if already_in_db:
                    logger.warn(
                        f"""LOGGER WARN / deleted word:
                        {already_in_db.unknown},
                        {already_in_db.known}""")  # to check
                    db.session.delete(already_in_db)
                    db.session.commit()
                    continue
    return user_file


def new_words_from_text_file():
    """appends new words from the text file to the database,
    if user_textfile.txt uploaded"""
    db.create_all()
    print(file_in_user_destination)
    print(file_in_sample_destination)

    if os.path.exists(file_in_user_destination):
        logger.warn(
                f"""LOGGER WARN / exists----------------------------:""")
        with open(file_in_user_destination) as user_file:
            user_file = _add(db, user_file)
        os.remove(file_in_user_destination)

    if len(VDP.models.Word.query.all()) < no_of_selected:
        with open(file_in_sample_destination) as user_file:
            logger.warn(
                f"""LOGGER WARN / words added from sample:""")  # to check
            user_file = _add(db, user_file)
    else:
        logger.warn(
            f"""LOGGER WARN / No other words added to the
            \'VDP.models.Word\' table.
            """)  # to check
    print(user_file)

    return user_file


def show_all_words_from_database():
    all_words_list = []
    try:
        all_words = VDP.models.Word.query.all()
        for w in all_words:
            all_words_list.append((w.unknown, w.known, w.level))
    except OperationalError:
        pass
    logger.warn(
            f"""LOGGER WARN / All words in the database:
            {all_words_list}""")  # to check
    return all_words_list


def select_word_to_test():
    """slects random words from the database according to algorithm"""
    logger.warn(f"""LOGGER WARN / selecting random words:""")  # to check
    q = db.session.query(VDP.models.Word)
    chosen_list.clear()
    while len(chosen_list) < no_of_selected:
        rand = randrange(0, q.count())
        row = db.session.query(VDP.models.Word)[rand]
        if (row.unknown, row.known, row.id) not in chosen_list:
            chosen_list.append((row.unknown, row.known, row.id))
            continue
    logger.warn(f"""LOGGER WARN / chosen_list: {chosen_list}.""")  # to check
    return chosen_list


def prepare_game():
    """starts the game - creates the connection to database,
    imports words from text file and chooses list of words for the play"""
    new_words_from_text_file()
    show_all_words_from_database()
    chosen_list = select_word_to_test()
    return chosen_list


def evaluate_game(form_words, word_ids):
    """checks, if the data input from the user
    corresponds to the chosen words' translation"""
    final_list_comparison = []
    idx = 0
    for w_id in word_ids:
        orig_word = VDP.models.Word.query.filter_by(id=w_id).first()
        tup = (
            orig_word.unknown, orig_word.known, form_words[idx],
            form_words[idx] == orig_word.known)
        final_list_comparison.append(tup)
        idx += 1
    return final_list_comparison


def end_game():
    """deletes the database"""
    os.remove(APP_ROOT + '/' + db_name)     # to be removed in ver. 2
    logger.warn(f"""LOGGER WARN / removed: {db_name}""")  # to check
