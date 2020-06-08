#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-25 17:25:12
# @Last modified by:   Arrack
# @Last Modified time: 2020-06-08 15:27:48
#

from wtforms import BooleanField
from wtforms import Form
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import HiddenField

from wtforms.validators import DataRequired
from wtforms.validators import Length


class LoginForm(Form):
    email = StringField(
        label='Email',
        validators=[DataRequired(), Length(1, 64)])
    password = PasswordField(
        label='Password',
        validators=[DataRequired(), Length(1, 128)])
    remember_me = BooleanField('Remember me.')
    submit = SubmitField()


class TalkForm(Form):
    content = TextAreaField(validators=[DataRequired()])
    private = BooleanField()
    submit = SubmitField()


class ArticleForm(Form):
    title = StringField(validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired()])
    # time = StringField('datetime', validators=[DataRequired()])
    tags = StringField()
    newTags = StringField()
    category = HiddenField()
    tags = HiddenField()
    # url_name = StringField('urlName', validators=[DataRequired()])

    # save_draft = SubmitField('save')
    submit = SubmitField()
