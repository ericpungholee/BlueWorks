from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, TextAreaField, RadioField, FieldList, FloatField, FormField
from wtforms.validators import DataRequired, Length, Email,Optional, EqualTo, ValidationError, URL
from blueworks.models import Company, Consumer

class AccountType(FlaskForm):
    type = RadioField('Account Type', choices=[('consumer', 'Consumer'), ('company', 'Company')])
    submit = SubmitField('Next')

class RegistrationForm_Consumer(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    location_country = StringField('Country', validators=[DataRequired(), Length(max=50)])
    location_province = StringField('Province', validators=[DataRequired(), Length(max=50)])
    location_city = StringField('City', validators=[DataRequired(), Length(max=50)])
    address = StringField('Address', validators=[DataRequired(), Length(max=100)])
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Register')

    def validate_username(self, username):
        consumer = Consumer.query.filter_by(username=username.data).first()
        company = Company.query.filter_by(username=username.data).first()
        if consumer or company:
            raise ValidationError('That Username is already taken. Please choose a diffrent one.')

    def validate_email(self, email):
        consumer = Consumer.query.filter_by(email=email.data).first()
        if consumer:
            raise ValidationError('That email is taken. Please choose a different one.')
class SingleLinkForm(FlaskForm):
    link = StringField('Link', validators=[Optional(), URL(), Length(max=120)])


class RegistrationForm_Company(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    location_country = StringField('Country', validators=[DataRequired(), Length(max=50)])
    location_province = StringField('Province', validators=[DataRequired(), Length(max=50)])
    location_city = StringField('City', validators=[DataRequired(), Length(max=50)])
    address = StringField('Address', validators=[DataRequired(), Length(max=100)])
    logo = FileField('Logo', validators=[FileAllowed(['jpg', 'png'])])
    licenses = StringField('Licenses', validators=[Length(max=500)])
    company_type = RadioField(
    'Company Type', 
    choices=[
        ('plumber', 'Plumber'.capitalize()), 
        ('electrician', 'Electrician'.capitalize()), 
        ('carpenter', 'Carpenter'.capitalize()), 
        ('handyman', 'Handyman'.capitalize())
    ], 
    validators=[DataRequired()]
)
    bio = StringField('Bio', validators=[Length(max=500)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=70)])
    links = FieldList(FormField(SingleLinkForm), min_entries=1, label='Links')
    submit = SubmitField('Register')

    def validate_username(self, username):
        company = Company.query.filter_by(username=username.data).first()
        consumer = Consumer.query.filter_by(username=username.data).first()
        if company or consumer:
            raise ValidationError('That Username is already taken. Please choose a different one.')

    def validate_email(self, email):
        company = Company.query.filter_by(email=email.data).first()
        if company:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateProfileConsumer(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    location_country = StringField('Country', validators=[DataRequired(), Length(max=50)])
    location_province = StringField('Province', validators=[DataRequired(), Length(max=50)])
    location_city = StringField('City', validators=[DataRequired(), Length(max=50)])
    address = StringField('Address', validators=[DataRequired(), Length(max=100)])
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

class UpdateProfileCompany(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    location_country = StringField('Country', validators=[DataRequired(), Length(max=50)])
    location_province = StringField('Province', validators=[DataRequired(), Length(max=50)])
    location_city = StringField('City', validators=[DataRequired(), Length(max=50)])
    address = StringField('Address', validators=[DataRequired(), Length(max=100)])
    logo = FileField('Logo', validators=[FileAllowed(['jpg', 'png'])])
    licenses = StringField('Licenses', validators=[Length(max=500)])
    company_type = RadioField(
    'Company Type', 
    choices=[
        ('plumber', 'Plumber'.capitalize()), 
        ('electrician', 'Electrician'.capitalize()), 
        ('carpenter', 'Carpenter'.capitalize()), 
        ('handyman', 'Handyman'.capitalize())
    ], 
    validators=[DataRequired()]
)

    bio = StringField('Bio', validators=[Length(max=1100)])
    links = FieldList(FormField(SingleLinkForm), min_entries=1, label='Links')
    phone = StringField('Phone', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Update')

class SearchForm(FlaskForm):
    searched = StringField('Searched', validators=[DataRequired()])
    submit = SubmitField('Search')

class PortfolioForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=3000)])
    picture_1 = FileField('Upload Pictures', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    picture_2 = FileField('Upload Pictures', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    picture_3 = FileField('Upload Pictures', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    picture_4 = FileField('Upload Pictures', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    picture_5 = FileField('Upload Pictures', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    picture_6 = FileField('Upload Pictures', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    picture_7 = FileField('Upload Pictures', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    picture_8 = FileField('Upload Pictures', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    picture_9 = FileField('Upload Pictures', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    picture_10 = FileField('Upload Pictures', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField('Add')

class ReviewForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=8, max=500)])
    submit = SubmitField()


class RateCompanyForm(FlaskForm):
    rating = FloatField('Rating', validators=[
        validators.InputRequired(), 
        validators.NumberRange(min=0.0, max=5.0, message="Rating should be between 0 and 5")
    ])
    submit = SubmitField('Rate')