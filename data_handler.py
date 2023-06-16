import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class DataHandler:
    def __init__(self, database_url, credential_path):
        # Initialize the Firebase app with the provided credentials
        cred = credentials.Certificate(credential_path)
        firebase_admin.initialize_app(cred, {'databaseURL': database_url})

    def insert_or_update_user_schema(self, user_schema):
        # Get a reference to the 'user' collection in the database
        ref = db.reference('User')
        user_data = ref.get()

        if user_data is not None and user_schema["uuid"] in user_data:
            # User exists, update the row with the new user schema data
            ref.child(user_schema["uuid"]).update(user_schema)
        else:
            # User does not exist, insert a new row with the user schema data
            ref.child(user_schema["uuid"]).set(user_schema)

    def insert_training_schema(self, training_schema):
        # Get a reference to the 'training' collection in the database
        ref = db.reference('Training Data')
        # Push the training schema data as a new child under 'training'
        ref.push(training_schema)

    def process_data_and_save(self, patient, answers):
        # Convert the answers to user schema and training schema values
        user_schema_values = self.get_user_schema_values(patient, answers)
        training_schema_values = self.get_training_schema_values(answers)

        # Insert or update the user schema in the database
        self.insert_or_update_user_schema(user_schema_values)
        # Insert the training schema in the database
        self.insert_training_schema(training_schema_values)

    def get_user_schema_values(self, patient, answers):
        # Extract the relevant user schema values from the answers
        return {
            "uuid": patient.get("uuid"),
            "email": patient.get("email"),
            "age": answers.get("age"),
            "dietary_preferences": answers.get("dietary_preferences"),
            "alcohol_consumption": answers.get("alcohol_consumption"),
            "tobacco_use": answers.get("tobacco_use")
        }

    def get_training_schema_values(self, answers):
        # Extract the relevant training schema values from the answers
        return {
            "symptoms": answers.get("symptoms"),
            "symptoms_duration": answers.get("symptoms_duration"),
            "medications": answers.get("medications"),
            "health_history": answers.get("health_history")
        }
