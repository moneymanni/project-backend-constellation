from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField
from wtforms.validators import DataRequired

class LinkInfoCreateForm(FlaskForm):
    pageId = IntegerField("pageId", validators=[DataRequired()])
    linkedPageId = IntegerField("linkedPageId", validators=[DataRequired()])
    linkage = FloatField("linkage", validators=[DataRequired()])

class LinkInfoDeleteForm(FlaskForm):
    pageId = IntegerField("pageId", validators=[DataRequired()])
    linkedPageId = IntegerField("linkedPageId", validators=[DataRequired()])