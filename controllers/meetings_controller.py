from flask import request
from datetime import datetime, timezone

def add_meeting(db):
    data = request.get_json()

    if 'title' not in data or not data['title']:
        return {'msg': 'Missing required field: title'}, 400

    meeting_data = {
        'title': data['title'],
        'transcript': data.get('transcript', ''),
        'meetingNote': data.get('meetingNote', ''),
        'summary': data.get('summary', ''),
        'keywords': data.get('keywords', []),
        'createdAt': datetime.now(timezone.utc),
        'lastUpdated': datetime.now(timezone.utc)
    }

    doc_ref = db.collection('meetings').add(meeting_data)

    return {'id': doc_ref[1].id, 'msg': 'created'}, 201

def get_meetings(db):
    meetings = []
    for doc in db.collection('meetings').stream():
        meeting = doc.to_dict()
        meeting['id'] = doc.id

        # 把 datetime 物件轉成 ISO8601 字串，避免 JSON 序列化問題
        for time_field in ['createdAt', 'lastUpdated']:
            if time_field in meeting and meeting[time_field]:
                # Firestore 儲存的 timestamp 可能是 datetime 物件或 firestore.Timestamp 物件，要小心轉換
                try:
                    meeting[time_field] = meeting[time_field].isoformat()
                except AttributeError:
                    # 如果不是 datetime，嘗試用 to_datetime
                    try:
                        meeting[time_field] = meeting[time_field].to_datetime().isoformat()
                    except Exception:
                        pass  # 保持原本格式

        meetings.append(meeting)

    return meetings, 200


def get_meeting(db, meeting_id: str):
    doc_ref = db.collection('meetings').document(meeting_id)
    doc = doc_ref.get()
    if not doc.exists:
        return {'msg': 'Meeting not found'}, 404

    meeting = doc.to_dict()
    meeting['id'] = doc.id

    for time_field in ['createdAt', 'lastUpdated']:
        if time_field in meeting and meeting[time_field]:
            try:
                meeting[time_field] = meeting[time_field].isoformat()
            except AttributeError:
                try:
                    meeting[time_field] = meeting[time_field].to_datetime().isoformat()
                except Exception:
                    pass

    return meeting, 200

def delete_meeting(db, meeting_id: str):
    doc_ref = db.collection('meetings').document(meeting_id)
    doc = doc_ref.get()
    if not doc.exists:
        return {'msg': 'Meeting not found'}, 404

    doc_ref.delete()
    return {'msg': 'Meeting deleted'}, 200
