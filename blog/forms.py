from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import (
    BooleanField, StringField, SubmitField, SelectField, PasswordField, FileField
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
    submit = SubmitField('Log in')


class UpdateForm(FlaskForm):
    title = StringField(
        label='Title',
        validators=[DataRequired(), Length(1, 60)])
    category = SelectField(
        label='Category',
        choices=[(4, '随笔'), (2, '技术'), (3, '资讯'), (1, '其他')],
        coerce=int,
        default=1)
    tag = StringField(
        label='tag',
        validators=[DataRequired(), Length(1, 256)])
    markdown = FileField(
        label='Markdown-file',
        validators=[FileRequired(), FileAllowed(['md'], 'Only .md')])
    submit = SubmitField()
