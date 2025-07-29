from flask import request
from helpers.whisperx_helper import transcribe_mp3_to_text
from datetime import datetime, timezone
import os

def upload_and_transcribe(db, meeting_id):
    # 先檢查 meeting 是否存在
    meeting_doc_ref = db.collection('meetings').document(meeting_id)
    meeting_doc = meeting_doc_ref.get()
    if not meeting_doc.exists:
        return {"error": "Meeting not found"}, 404

    file = request.files.get('file')
    if not file:
        return {"error": "No file uploaded"}, 400

    # 確保 uploads 資料夾存在
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # 儲存 mp3 檔案到本地
    mp3_path = os.path.join(upload_dir, file.filename)
    file.save(mp3_path)

    # 轉錄 mp3 成文字
    transcript_text = transcribe_mp3_to_text(mp3_path)

    # 更新 meetings 文件的 transcript 欄位
    meeting_doc_ref.update({
        'transcript': transcript_text,
        'lastUpdated': datetime.now(timezone.utc)
    })

    # 刪除本地暫存檔案
    os.remove(mp3_path)

    return {"transcript": transcript_text}

def add_transcript(db, meeting_id):
    data = request.get_json()
    data['meeting_id'] = meeting_id
    doc_ref = db.collection('meeting_transcripts').add(data)
    return {'id': doc_ref[1].id, 'msg': 'created'}, 201