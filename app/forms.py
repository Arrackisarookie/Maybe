from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, StringField, SubmitField, PasswordField, TextAreaField
)
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[DataRequired(), Length(1, 64)])
    password = PasswordField(
        label='Password',
        validators=[DataRequired(), Length(1, 128)])
    remember_me = BooleanField('Remember me.')
    submit = SubmitField('Login')


class TalkForm(FlaskForm):
    content = TextAreaField(validators=[DataRequired()])
    private = BooleanField()
    submit = SubmitField()