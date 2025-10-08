from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from wtforms import Form, SelectMultipleField, IntegerField, TextAreaField, SubmitField
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, IntegerField, BooleanField
from wtforms.validators import NumberRange


class RegistrationForm(FlaskForm):
    # Field names match the input names in register.html (email, password, name)
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    remember = BooleanField('Remember Me')  # <-- add this field
    submit = SubmitField('Login')



class NewBookForm(FlaskForm):
    title = StringField("Title:", validators=[DataRequired()])
    category = SelectField(
        "Choose a Category:",
        choices=[("Children", "Children"), ("Teens", "Teens"), ("Adults", "Adults")],
        validators=[DataRequired()]
    )
    genres = SelectMultipleField(
        "Choose multiple Genres:",
        choices=[(g, g) for g in [
            "Animals", "Business", "Comics", "Communication", "Dark Academia",
            "Emotion", "Fantasy", "Fiction", "Friendship", "Graphic Novels", "Grief",
            "Historical Fiction", "Indigenous", "Inspirational", "Magic", "Mental Health",
            "Nonfiction", "Personal Development", "Philosophy", "Picture Books", "Poetry",
            "Productivity", "Psychology", "Romance", "School", "Self Help"
        ]],
        validators=[DataRequired()]
    )
    url = StringField("URL for cover:", validators=[DataRequired()])
    description = TextAreaField("Description:", validators=[DataRequired()])
    pages = IntegerField("Number of Pages:", validators=[DataRequired(), NumberRange(min=1)])
    copies = IntegerField("Number of Copies:", validators=[DataRequired(), NumberRange(min=1)])
    
    # Authors & Illustrator checkboxes
    author1 = StringField("Author 1:", validators=[DataRequired()])
    illustrator1 = BooleanField("Illustrator")
    author2 = StringField("Author 2:")
    illustrator2 = BooleanField("Illustrator")
    author3 = StringField("Author 3:")
    illustrator3 = BooleanField("Illustrator")
    author4 = StringField("Author 4:")
    illustrator4 = BooleanField("Illustrator")
    author5 = StringField("Author 5:")
    illustrator5 = BooleanField("Illustrator")

