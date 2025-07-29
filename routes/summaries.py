from flask_restful import Resource
from controllers.summaries_controller import add_summary

class SummariesResource(Resource):
    def __init__(self, db):
        self.db = db

    def post(self, meeting_id):
        return add_summary(self.db, meeting_id)