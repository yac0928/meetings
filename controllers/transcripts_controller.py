from flask import request
from helpers.whisperx_helper import transcribe_mp3_to_text
from controllers.meetings_controller import get_meeting
from helpers.gemini import gemini_api_call
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

def get_transcript(db, meeting_id):
    meeting = get_meeting(db, meeting_id)
    transcripts = meeting[0]['transcript']
    return transcripts, 200

def improve_transcript(db, meeting_id):
    meeting_doc_ref = db.collection('meetings').document(meeting_id)
    meeting_doc = meeting_doc_ref.get()
    if not meeting_doc.exists:
        return {'msg': 'Meeting not found'}, 404
    
    transcript, status = get_transcript(db, meeting_id)
    if status != 200:
        return {"error": "無法取得逐字稿"}, status
    combined_transcript = "\n".join([segment['text'] for segment in transcript])
    prompt = "transcripts是老師與學生的會議，語音轉文字的逐字稿，請幫我改善轉換不順的逐字稿，讓它更通順易懂，並且保留原意。回傳格式僅僅為改善後的逐字稿，不要回答其他任何內容。"
    all_prompt = f"transcript: {combined_transcript}\n{prompt}"
    improved_transcript = gemini_api_call(all_prompt)
    meeting_doc_ref.update({
        'improvedTranscript': improved_transcript,
        'lastUpdated': datetime.now(timezone.utc)
    })
    return improved_transcript, 200

