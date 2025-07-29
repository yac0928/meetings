from flask_restful import Resource
from controllers.meetings_controller import add_meeting, get_meetings, get_meeting, delete_meeting

class MeetingsResource(Resource):
    def __init__(self, db):
        self.db = db

    def get(self):
        return get_meetings(self.db)

    def post(self):
        return add_meeting(self.db)


class MeetingResource(Resource):
    def __init__(self, db):
        self.db = db

    def get(self, meeting_id):
        return get_meeting(self.db, meeting_id)
    
    def delete(self, meeting_id):
        return delete_meeting(self.db, meeting_id)