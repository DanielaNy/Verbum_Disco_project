from wtforms import Form, validators
from wtforms import BooleanField, StringField
from wtforms import SubmitField, PasswordField, HiddenField   # to be checked
from flask_wtf import FlaskForm
from VDP.game import chosen_list


class TranslationForm(FlaskForm):
    word1 = StringField(chosen_list[0][0])
    word2 = StringField(chosen_list[1][0])
    word3 = StringField(chosen_list[2][0])
    word4 = StringField(chosen_list[3][0])
    word5 = StringField(chosen_list[4][0])
    word_ids = HiddenField()
    submit = SubmitField('Submit')
