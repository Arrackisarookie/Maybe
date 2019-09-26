from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import (
    BooleanField, StringField, SubmitField, SelectField, PasswordField,
    FileField
)
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(1, 128)])
    remember_me = BooleanField('Remember me.')
    submit = SubmitField('Log in')


class UpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    # category = SelectField('Category', coerce=int, default=1)
    markdown = FileField('Markdown-file', validators=[
        FileRequired(), FileAllowed(['md'], 'Only .md')])
    submit = SubmitField()
