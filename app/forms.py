from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from models.models import User

class RegistrationForm(FlaskForm):
    user_name = StringField('UserName', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    conform_password = PasswordField('conform password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('ユーザー登録')
    
    def validate_username(self, user_name):
        user = User.query.filter_by(user_name=user_name.data).one_or_none()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).one_or_none()
        if user is not None:
            raise ValidationError('Please use a different email.')

class LoginForm(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('ログイン')
        
