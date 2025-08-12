from flask_restful import Resource
from controllers.transcripts_controller import add_transcript, upload_and_transcribe, get_transcript, improve_transcript

class TranscriptsResource(Resource):
    def __init__(self, db):
        self.db = db
    
    def get(self, meeting_id):
        return get_transcript(self.db, meeting_id)

    def post(self, meeting_id):
        # 上傳文字檔（JSON 格式）
        return add_transcript(self.db, meeting_id)
    
    def put(self, meeting_id):
        # 改善逐字稿
        return improve_transcript(self.db, meeting_id)

class TranscriptsUploadResource(Resource):
    def __init__(self, db):
        self.db = db

    def post(self, meeting_id):
        # 上傳語音檔（multipart/form-data）
        return upload_and_transcribe(self.db, meeting_id)