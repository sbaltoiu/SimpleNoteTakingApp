# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import User

class NoteForm(FlaskForm):
    """
    Form for normal user to add or edit a note
    """
    noteText = StringField('Note text', validators=[DataRequired()])
    submit = SubmitField('Submit')