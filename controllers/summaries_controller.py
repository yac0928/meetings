from flask import request
from datetime import datetime, timezone
from helpers.gemini import gemini_api_call


def put_summary(db, meeting_id):
    meeting_doc_ref = db.collection('meetings').document(meeting_id)
    meeting_doc = meeting_doc_ref.get()
    if not meeting_doc.exists:
        return {'msg': 'Meeting not found'}, 404
    
    improved_transcript = meeting_doc.to_dict()['improvedTranscript']
    prompt = "請幫我整理這段老師與學生會議（transcripts）的全部重點筆記，內容要清楚且易懂，適合資工所碩一新生學習理解。重點應包含主要議題、結論及重要提醒。**回答時不要有客套語、解釋或多餘文字，只要用嚴謹的筆記格式輸出，方便直接存進資料庫。**"
    all_prompt = f"transcript: {improved_transcript}\n{prompt}"
    summary = gemini_api_call(all_prompt)

    meeting_doc_ref.update({
        'summary': summary,
        'lastUpdated': datetime.now(timezone.utc)
    })

    return {'msg': 'Summary added', 'summary': summary}, 200
