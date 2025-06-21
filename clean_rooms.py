import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# Load your Firebase credentials from environment variable or local file
cred_json = os.environ.get("FIREBASE_CREDS_JSON")

if cred_json:
    cred = credentials.Certificate(json.loads(cred_json))
else:
    # Alternative: Use a local service account JSON file path if running locally
    cred = credentials.Certificate("firebase_creds.json")  # <-- change this to your file if needed

firebase_admin.initialize_app(cred)

db = firestore.client()

rooms_ref = db.collection('rooms').stream()

deleted = 0
for doc in rooms_ref:
    data = doc.to_dict()
    if 'name' not in data:
        db.collection('rooms').document(doc.id).delete()
        deleted += 1
        print(f"Deleted room: {doc.id}")

print(f"✅ Cleanup complete. {deleted} undefined rooms removed.")
