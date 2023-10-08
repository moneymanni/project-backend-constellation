from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class SignInForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Length(max=255)])
    password = PasswordField("password", validators=[DataRequired()])
