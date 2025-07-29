from flask import Flask
from flask_restful import Api
import firebase_admin
from firebase_admin import credentials, firestore

from routes import register_routes

app = Flask(__name__)
api = Api(app)

cred = credentials.Certificate('firebaseAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def hello():
    return 'Flask + Firebase 運作中！'

register_routes(api, db)

if __name__ == '__main__':
    app.run(debug=True)
