#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-25 17:25:12
# @Last modified by:   Arrack
# @Last Modified time: 2020-05-27 21:25:39
#

from wtforms import BooleanField
from wtforms import Form
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField

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
