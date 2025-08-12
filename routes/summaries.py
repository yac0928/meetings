from flask_restful import Resource
from controllers.summaries_controller import put_summary

class SummariesResource(Resource):
    def __init__(self, db):
        self.db = db

    def put(self, meeting_id):
        return put_summary(self.db, meeting_id)