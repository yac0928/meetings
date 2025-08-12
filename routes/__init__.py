from .meetings import MeetingsResource, MeetingResource
from .transcripts import TranscriptsResource, TranscriptsUploadResource
from .notes import NotesResource, NoteResource
from .summaries import SummariesResource
from .keywords import keywordsResource

def register_routes(api, db):
    api.add_resource(MeetingsResource, '/meetings', resource_class_kwargs={'db': db})
    api.add_resource(MeetingResource, '/meetings/<string:meeting_id>', resource_class_kwargs={'db': db})
    api.add_resource(TranscriptsResource, '/meetings/<string:meeting_id>/transcripts', resource_class_kwargs={'db': db})
    api.add_resource(TranscriptsUploadResource, '/meetings/<string:meeting_id>/transcripts/upload', resource_class_kwargs={'db': db})
    api.add_resource(NotesResource, '/meetings/<string:meeting_id>/notes', resource_class_kwargs={'db': db})
    api.add_resource(NoteResource, '/meetings/<string:meeting_id>/notes/<string:note_id>', resource_class_kwargs={'db': db})
    api.add_resource(SummariesResource, '/meetings/<string:meeting_id>/summaries', resource_class_kwargs={'db': db})
    api.add_resource(keywordsResource, '/meetings/<string:meeting_id>/keywords', resource_class_kwargs={'db': db})