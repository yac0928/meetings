from flask_restful import Resource
from controllers.keywords_controller import extract_keywords_from_transcript

class keywordsResource(Resource):
    def __init__(self, db):
        self.db = db

    def put(self, meeting_id):
        return extract_keywords_from_transcript(self.db, meeting_id)