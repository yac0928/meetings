from flask import request
from datetime import datetime, timezone
from helpers.ollama import analyze_transcript_with_ollama


def add_summary(db, meeting_id):
    meeting_doc_ref = db.collection('meetings').document(meeting_id)
    meeting_doc = meeting_doc_ref.get()
    if not meeting_doc.exists:
        return {'msg': 'Meeting not found'}, 404

    meeting_data = meeting_doc.to_dict()
    transcript_text = meeting_data.get('transcript')
    if not transcript_text:
        return {'msg': 'Transcript not found'}, 404

    summary = analyze_transcript_with_ollama(transcript_text)

    meeting_doc_ref.update({
        'summary': summary,
        'lastUpdated': datetime.now(timezone.utc)
    })

    return {'msg': 'Summary added', 'summary': summary}, 200
