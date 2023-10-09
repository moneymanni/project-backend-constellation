from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class NoteInfoCreateForm(FlaskForm):
    title = StringField("title", validators=[DataRequired(), Length(max=255)])
    description = StringField("description", validators=[DataRequired(), Length(max=2000)])
    sharedPermission = IntegerField("sharedPermission", validators=[DataRequired(), NumberRange(min=1, max=2)])

class NoteInfoUpdateForm(FlaskForm):
    title = StringField("title", validators=[DataRequired(), Length(max=255)])
    description = StringField("description", validators=[DataRequired(), Length(max=2000)])
    noteId = IntegerField("noteId", validators=[DataRequired()])
    sharedPermission = IntegerField("sharedPermission", validators=[DataRequired(), NumberRange(min=1, max=2)])

class NoteInfoDeleteForm(FlaskForm):
    noteId = IntegerField("noteId", validators=[DataRequired()])
