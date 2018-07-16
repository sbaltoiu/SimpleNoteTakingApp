# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import NoteForm
from .. import db
from ..models import Note, User

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Note Views

@admin.route('/notes', methods=['GET', 'POST'])
@login_required
def list_notes():
    """
    List all notes
    """
    check_admin()

    notes = Note.query.all()

    return render_template('admin/notes/notes.html',
                           notes=notes, title="Notes")

@admin.route('/notes/add', methods=['GET', 'POST'])
@login_required
def add_note():
    """
    Add a note to the database
    """
    check_admin()

    add_note = True

    form = NoteForm()
    if form.validate_on_submit():
        note = Note(user_id=form.user.data.id, text=form.noteText.data)
        try:
            # add note to the database
            db.session.add(note)
            db.session.commit()
            flash('You have successfully added a new note.')
        except:
            flash('Note cannot be added.')
            db.session.rollback()

        # redirect to notes page
        return redirect(url_for('admin.list_notes'))

    # load note template
    return render_template('admin/notes/note.html', action="Add",
                           add_note=add_note, form=form,
                           title="Add Note")

@admin.route('/notes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    """
    Edit a note
    """
    check_admin()

    add_note = False

    note = Note.query.get_or_404(id)
    form = NoteForm(obj=note)
    if form.validate_on_submit():
#        note.userEmail = form.userEmail.data
        note.noteText = form.noteText.data
        db.session.commit()
        flash('You have successfully edited the note.')

        # redirect to the notes page
        return redirect(url_for('admin.list_notes'))

    form.noteText.data = note.text
    # form.userEmail.data = note.user_id
    return render_template('admin/notes/note.html', action="Edit",
                           add_note=add_note, form=form,
                           note=note, title="Edit Note")

@admin.route('/notes/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_note(id):
    """
    Delete a note from the database
    """
    check_admin()

    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    flash('You have successfully deleted the note.')

    # redirect to the notes page
    return redirect(url_for('admin.list_notes'))

    return render_template(title="Delete Note")

@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title='users')
