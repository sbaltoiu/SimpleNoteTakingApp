# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import User

class NoteForm(FlaskForm):
    """
    Form for admin to add or edit a note
    """
    user = QuerySelectField(query_factory=lambda: User.query.all(),
                                  get_label="email")
    noteText = StringField('Note text', validators=[DataRequired()])
    submit = SubmitField('Submit')