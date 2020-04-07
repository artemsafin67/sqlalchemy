from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email


class RegisterForm(FlaskForm):
    login_email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    password_again = PasswordField('Repeat password', validators=[InputRequired(), EqualTo("password")])
    surname = StringField('Surname', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    age = IntegerField('Age', validators=[InputRequired()])
    position = StringField('Position', validators=[InputRequired()])
    speciality = StringField('Speciality', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    submit = SubmitField("Зарегистрироваться")