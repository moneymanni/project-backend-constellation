from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length

class TagInfoCreateForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(max=255)])
    pageId = IntegerField("pageId", validators=[DataRequired()])


class LinkTagToFageForm(FlaskForm):
    pageId = IntegerField("pageId", validators=[DataRequired()])
    tagId = IntegerField("tagId", validators=[DataRequired()])

class TagInfoUpdateForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(max=255)])
    tagId = IntegerField("tagId", validators=[DataRequired()])


class TagInfoDeleteForm(FlaskForm):
    tag_id = IntegerField("tag_id", validators=[DataRequired()])
