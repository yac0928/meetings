# transcripts = get_transcripts(db, meeting_id)
# prompt = (transcripts是老師與學生的會議，語音轉文字的逐字稿，先幫我優化轉換失敗的文字，再幫我判斷每句話的講者，接著幫我萃取每句話的關鍵詞與解釋，最後將所有關鍵詞去重，並回傳格式為 [{'keyword': ..., 'explanation': ...}, ...] 的列表。)
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key = os.getenv('GEMINI_API_KEY'))

def gemini_api_call(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        # 直接回傳 text 屬性
        return response.text
    except Exception as e:
        # 捕捉並拋出錯誤詳訊
        raise Exception(f"Gemini API call failed: {e}")
