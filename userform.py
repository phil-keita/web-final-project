from flask_wtf import FlaskForm, Form
from wtforms.fields import StringField, SubmitField, EmailField, SelectField, FieldList, FormField, IntegerField
from wtforms.validators import InputRequired, Email, Length, EqualTo, NumberRange, Optional

class Register_Form(FlaskForm):
    username = StringField("Username ", validators=[InputRequired()])
    email = EmailField("Email ", validators=[InputRequired(), Email()])
    password = StringField("Password", validators=[InputRequired(), Length(min=8, max=30, message="Invalid Length. (Must be between 8 and 30 characters)"), EqualTo("confirm_password", message="Passwords do not match.")])
    confirm_password = StringField("Confirm Password", validators=[InputRequired(), Length(min=8, max=30, message="Invalid Length. (Must be between 8 and 30 characters)")])
    submit = SubmitField("Submit")

class Login_form(FlaskForm):
    username = StringField("Username ", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    submit = SubmitField("Submit")

class PrePostForm(FlaskForm):
    num_ingredients = IntegerField("Number of ingredients: ", validators=[InputRequired(), NumberRange(min=1)])
    units = SelectField("Which units will you be using: ", choices=("Metric", "Imperial"), validators=[InputRequired()] )
    submit = SubmitField("Submit")



class IngrediantForm(Form):
    name = StringField('Ingrediant:', validators=[InputRequired()])
    quantity = IntegerField('Quantity:' , validators=[InputRequired(), NumberRange(min=1)])


class Post_Form(FlaskForm):
    post_name = StringField("Title ", validators=[InputRequired()])
    ingredients = FieldList(FormField(IngrediantForm), min_entries=1)
    recipe = StringField("Enter Recipe Here ", validators=[InputRequired()])
    im_units = SelectField('Units:', choices=('tsp', 'tbsp', 'floz', 'cup', 'gal', 'oz', 'lb'), validators=[Optional()])
    m_units = SelectField('Units:', choices=('ml', 'l', 'mg', 'g', 'kg'), validators=[Optional()])
    submit = SubmitField("Post")
    #TODO: ADD HERE IF NEEDED

class Comment_Form(FlaskForm):
    text = StringField("Text ")
    rating = SelectField("Rating ", choices=[(1, "One Star"), (2, "Two Stars"), (3, "Three Stars"), (4, "Four Stars"), (5, "Five Stars")], validators=[InputRequired()])
    submit = SubmitField("Comment")
    #TODO: ADD HERE IF NEEDED

        


