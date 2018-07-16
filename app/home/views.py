# app/home/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import home
from forms import NoteForm
from .. import db
from ..models import Note, User

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")

# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

@home.route('/notes', methods=['GET', 'POST'])
@login_required
def list_notes():
    """
    List all notes
    """

    notes = Note.query.all()
    notes = [note for note in notes if note.user_id == current_user.id]

    return render_template('home/notes/notes.html',
                           notes=notes, title="Notes")

@home.route('/notes/add', methods=['GET', 'POST'])
@login_required
def add_note():
    """
    Add a note to the database
    """

    add_note = True

    form = NoteForm()
    if form.validate_on_submit():
        note = Note(user_id=current_user.id, text=form.noteText.data)
        try:
            # add note to the database
            db.session.add(note)
            db.session.commit()
            flash('You have successfully added a new note.')
        except:
            flash('Note cannot be added.')
            db.session.rollback()

        # redirect to notes page
        return redirect(url_for('home.list_notes'))

    # load note template
    return render_template('home/notes/note.html', action="Add",
                           add_note=add_note, form=form,
                           title="Add Note")

@home.route('/notes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    """
    Edit a note
    """

    add_note = False

    note = Note.query.get_or_404(id)
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.user_id = current_user.id
        note.noteText = form.noteText.data
        db.session.commit()
        flash('You have successfully edited the note.')

        # redirect to the notes page
        return redirect(url_for('home.list_notes'))

    form.noteText.data = note.text
    # form.userEmail.data = note.user_id
    return render_template('home/notes/note.html', action="Edit",
                           add_note=add_note, form=form,
                           note=note, title="Edit Note")

@home.route('/notes/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_note(id):
    """
    Delete a note from the database
    """

    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    flash('You have successfully deleted the note.')

    # redirect to the notes page
    return redirect(url_for('home.list_notes'))

    return render_template(title="Delete Note")