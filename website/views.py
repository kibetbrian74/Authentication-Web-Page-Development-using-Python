from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import current_user, login_required
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if note is None:
            flash('Note is empty!', category="Error")
        elif len(note) < 1:
            flash('Note is too short!', category='Error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note recorded!', category="Success")

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    noteData = json.loads(request.data)
    noteId = noteData['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
                db.session.delete(note)
                db.session.commit()
            
    return jsonify({})