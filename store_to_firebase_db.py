import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request, jsonify

# Initialize Firebase Admin SDK
cred = credentials.Certificate("healthcare-chat-gpt-firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://healthcare-chat-gpt-default-rtdb.firebaseio.com/'
})

# Get a reference to the Firebase Realtime Database
ref = db.reference()

app = Flask(__name__)


@app.route('/patients', methods=['POST'])
def store_data():
    # Retrieve data from the request
    data = request.json

    # Extract the required data fields
    patient_id = data["patient_id"]
    patient_name = data["patient_name"]
    conversation_history = data["conversation_history"]
    location = data["location"]
    appointment_types = data["appointment_types"]
    health_history = data["health_history"]

    # Create the data dictionary
    data_to_store = {
        "patient_id": patient_id,
        "patient_name": patient_name,
        "conversation_history": conversation_history,
        "location": {
            "latitude": location["latitude"],
            "longitude": location["longitude"]
        },
        "appointment_types": appointment_types,
        "health_history": health_history
    }

    # Store the data in the Firebase Realtime Database
    new_user_ref = ref.child("patients").push()
    new_user_ref.set(data_to_store)

    return jsonify({"message": "Data stored successfully"})


if __name__ == '__main__':
    app.run()
