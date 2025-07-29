from flask_restful import Resource
from controllers.notes_controller import (
    add_note, update_note, delete_note
)

class NotesResource(Resource):
    def __init__(self, db):
        self.db = db

    def post(self, meeting_id):
        return add_note(self.db, meeting_id)

class NoteResource(Resource):
    def __init__(self, db):
        self.db = db

    def put(self, meeting_id, note_id):
        return update_note(self.db, note_id)

    def delete(self, meeting_id, note_id):
        return delete_note(self.db, note_id)