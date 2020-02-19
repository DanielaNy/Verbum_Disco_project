from VDP import app, APP_ROOT, bootstrap, db, logger
from VDP import models, game
import os
from random import choice
from flask import render_template, request, redirect, url_for


@app.route("/")
def index():
    img_root = os.path.join(APP_ROOT, "static/images/index/")
    random_image = choice([
        x for x in os.listdir(img_root)
        if os.path.isfile(os.path.join(img_root, x))])
    logger.warn(f"""LOGGER WARN / random image: {random_image}""")  # to check
    return render_template(
        "index.html",
        random_image=random_image, img_root=img_root)


@app.route("/my_dictionary/")
def my_dictionary():
    all_words_list = game.show_all_words_from_database()
    if all_words_list:
        return render_template("my_dictionary.html",
            all_words_list=all_words_list)
    else:
        return render_template("my_dictionary_empty.html")


@app.route("/how_to/")
def how_to():
    return render_template("how_to.html", no_of_selected=game.no_of_selected)


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
    game.save_uploaded_file()
    return render_template("upload_completed.html")


@app.route("/play/", methods=['GET'])
def play():
    chosen_list = game.prepare_game()
    chosen_word_ids = ','.join(str(word[2]) for word in chosen_list)
    from VDP.forms import TranslationForm
    form = TranslationForm(word_ids=chosen_word_ids)
    return render_template("play.html", chosen_list=chosen_list, form=form)


@app.route('/result/', methods=['POST'])
def result():
    points = 0
    form_words = [
        request.form["word1"],
        request.form["word2"],
        request.form["word3"],
        request.form["word4"],
        request.form["word5"]]
    # for later comparing word and input in form 
    word_ids = request.form["word_ids"].split(",")
    # chosen list plus input from form and evaluation, if the input matches chosen word:
    final_list_comparison = game.evaluate_game(form_words, word_ids)
    # if match, points assigned
    for word_set in final_list_comparison:
        if word_set[3]:
            points += 1
    logger.warn(f"""LOGGER WARN / final_list_comparison:
        {final_list_comparison}""")  # to check
    return render_template("result.html",
        final_list_comparison=final_list_comparison, points=points)


@app.route('/end/')
def end():
    game.end_game()
    return render_template("end.html")
