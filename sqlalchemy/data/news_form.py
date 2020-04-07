from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import InputRequired


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[InputRequired()])
    content = TextAreaField('Содержание')
    is_private = BooleanField('Личное')
    submit = SubmitField('Добавить')
