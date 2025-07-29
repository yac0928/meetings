from flask import request
from datetime import datetime, timezone


def add_note(db, meeting_id):
    data = request.get_json()
    if not data or 'meetingNote' not in data:
        return {'msg': 'Missing meetingNote field'}, 400

    doc_ref = db.collection('meetings').document(meeting_id)
    doc = doc_ref.get()
    if not doc.exists:
        return {'msg': 'Meeting not found'}, 404

    meeting = doc.to_dict()
    if meeting.get('meetingNote'):
        return {'msg': 'Note already exists, use PUT to update'}, 409

    doc_ref.update({
        'meetingNote': data['meetingNote'],
        'lastUpdated': datetime.now(timezone.utc)
    })

    return {'msg': 'Note created'}, 201


def update_note(db, meeting_id):
    data = request.get_json()
    if not data or 'meetingNote' not in data:
        return {'msg': 'Missing meetingNote field'}, 400

    doc_ref = db.collection('meetings').document(meeting_id)
    doc = doc_ref.get()
    if not doc.exists or not doc.to_dict().get('meetingNote'):
        return {'msg': 'Note not found, use POST to create'}, 404

    doc_ref.update({
        'meetingNote': data['meetingNote'],
        'lastUpdated': datetime.now(timezone.utc)
    })

    return {'msg': 'Note updated'}, 200


def delete_note(db, meeting_id):
    doc_ref = db.collection('meetings').document(meeting_id)
    if not doc_ref.get().exists:
        return {'msg': 'Meeting not found'}, 404

    doc_ref.update({
        'meetingNote': '',
        'lastUpdated': datetime.now(timezone.utc)
    })

    return {'msg': 'Note deleted'}, 200