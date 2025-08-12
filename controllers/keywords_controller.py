from helpers.gemini import gemini_api_call
from datetime import datetime, timezone
import re
import json

def extract_keywords_from_transcript(db, meeting_id: str):
    meeting_doc_ref = db.collection('meetings').document(meeting_id)
    meeting_doc = meeting_doc_ref.get()
    if not meeting_doc.exists:
        return {'msg': 'Meeting not found'}, 404

    improved_transcript = meeting_doc.to_dict()['improvedTranscript']
    prompt = "transcripts是老師與學生的會議，請幫我萃取資工論文研究領域當中'艱澀的專有名詞'，幫助資工所碩一的新生理解會議內容，請不要小看他們，基本的名詞不需要提供(如Q&A, LLM, presentation, professor)，最後將所有關鍵詞去重並提供解釋，回傳格式僅僅為 [{'keyword': ..., 'explanation': ...}, { }, ...] 的json格式列表，我要直接存進資料庫。範例: [{'keyword': inductive coding, 'explanation': inductive coding是指從資料中歸納出概念或主題的過程。}]"
    all_prompt = f"transcript: {improved_transcript}\n{prompt}"
    keywords = gemini_api_call(all_prompt)
    string_json = keywords.split('```json')[1].split('```')[0]
    pure_json = string_json.replace('\n', '').replace('\\', '').strip()
    print(f"Extracted keywords: {pure_json}")
    keywords_json = json.loads(pure_json)

    meeting_doc_ref.update({
        'keywords': keywords_json,
        'lastUpdated': datetime.now(timezone.utc)
    })
    return {"keywords": keywords_json}, 200