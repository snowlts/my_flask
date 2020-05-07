from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, length, Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),length(1,64),Email()])
    password = PasswordField('password',validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class PasswdUpdateForm(FlaskForm):
    old_password = PasswordField('Old password',validators=[DataRequired()])
    password = PasswordField('New password',validators=[DataRequired(),EqualTo('password2',message='Password must match!')])
    password2 = PasswordField('Confirm new password',validators=[DataRequired()])
    submit = SubmitField('Update password')
    #
    def validate_password(self,field):
        if self.old_password.data == self.password.data:
            raise ValidationError('New password cannot be the same with the old one!')

# class EmailUpdateRequestForm(FlaskForm):
#     email = StringField('Email',validators=[DataRequired(), length(1,64), Email()])
#     verify_code = StringField(validators=[DataRequired(),length(6,6),Regexp('^[0-9]*$',0,message='validation code must have only numbers.')])
#     submit = SubmitField('Submit')

class EmailUpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), length(1, 64), Email()])
    verify_code = StringField(validators=[DataRequired(), length(6, 6),
                                          Regexp('^[0-9]*$', 0, message='validation code must have only numbers.')],description='Email validation code')
    # send_code = SubmitField('Send validation code')
    submit = SubmitField('Submit')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), length(1,64), Email()])
    submit = SubmitField('Send mail')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New password',validators=[DataRequired(),EqualTo('password2',message='Password must match!')])
    password2 = PasswordField('Confirm new password',validators=[DataRequired()])
    submit = SubmitField('Reset password')


class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), length(1,64), Email()])
    username = StringField('Username',validators=[DataRequired(),length(1,64),
                                                  Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                         message='Usernames must have only letters, numbers, dots or '
                                                         'underscores')])
    password = PasswordField('password',validators=[DataRequired(),EqualTo('password2',message='Password must match!')])
    password2 = PasswordField('Confirm password',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')



