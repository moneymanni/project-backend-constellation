from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length


class SignUpForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(),Length(max=255)])
    password = PasswordField("password", validators=[DataRequired()])
    profile = StringField("profile", validators=[DataRequired(), Length(max=2000)])

class UserInfoUpdateForm(FlaskForm):
    profile = StringField("profile", validators=[DataRequired(), Length(max=2000)])
