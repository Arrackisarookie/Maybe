from wtforms import (
    Form, BooleanField, StringField, SubmitField, PasswordField, TextAreaField
)
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    username = StringField(
        label='Username',
        validators=[DataRequired(), Length(1, 64)])
    password = PasswordField(
        label='Password',
        validators=[DataRequired(), Length(1, 128)])
    remember_me = BooleanField('Remember me.')
    submit = SubmitField('Login')


class TalkForm(Form):
    content = TextAreaField(validators=[DataRequired()])
    private = BooleanField()
    submit = SubmitField()
