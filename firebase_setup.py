import json, os
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    firebase_creds = json.loads(os.environ['FIREBASE_CREDS_JSON'])
    cred = credentials.Certificate(firebase_creds)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
