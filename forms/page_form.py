from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class PageInfoCreateForm(FlaskForm):
    noteId = IntegerField("noteId", validators=[DataRequired()])

class PageHeaderUpdateForm(FlaskForm):
    title = StringField("title", validators=[DataRequired(), Length(max=255)])
    keyword = StringField("keyword", validators=[DataRequired(), Length(max=255)])
    pageId = IntegerField("pageId", validators=[DataRequired()])

class PageContentUpdateForm(FlaskForm):
    content = StringField("content", validators=[DataRequired(), Length(max=2000)])
    pageId = IntegerField("pageId", validators=[DataRequired()])

class PageInfoDeleteForm(FlaskForm):
    pageId = IntegerField("pageId", validators=[DataRequired()])
