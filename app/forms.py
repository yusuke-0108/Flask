from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from models.models import User
from flask_wtf.file import FileAllowed

class RegistrationForm(FlaskForm):
    user_name = StringField('UserName', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    conform_password = PasswordField('conform password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('ユーザー登録')

class LoginForm(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('ログイン')
        
class EditForm(FlaskForm):
    user_name = StringField('UserName', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_img = FileField('profile', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Edit')