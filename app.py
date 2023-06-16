from flask import Flask, request, redirect, url_for
from flask_restful import Api, Resource
from flasgger import Swagger

import os
import requests
import json
from dotenv import load_dotenv
from prompt_processor import PromptProcessor
from data_handler import DataHandler
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)
from user import User

from oauthlib.oauth2 import WebApplicationClient


app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'
app.secret_key = os.getenv("SECRET_KEY") or os.urandom(24)
swagger = Swagger(app)
api = Api(app)
load_dotenv()

# Create an instance of the DataHandler class
data_handler = DataHandler('https://symptomassessmentchatbot-default-rtdb.firebaseio.com', 'symptomassessmentchatbot-firebase-adminsdk-vfk0y-82978d8fc5.json')

# Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

login_manager = LoginManager()
login_manager.init_app(app)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
        return requests.get(GOOGLE_DISCOVERY_URL).json()

class DoctorCategoryResource(Resource):
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id, data_handler)
    
    @app.route("/login")
    def login():
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)
    
    @app.route("/login/callback")
    def callback():
        code = request.args.get("code")
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )
        client.parse_request_body_response(json.dumps(token_response.json()))
        print("Token response", token_response.json())
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            picture = userinfo_response.json()["picture"]
            users_name = userinfo_response.json()["given_name"]
        else:
            return "User email not available or not verified by Google.", 400
        user = User(
            id_=unique_id, name=users_name, email=users_email, profile_pic=picture
        )

        #Not sure if it's standard practice to pass repo objects, but I'm going for the quickest approach
        #that won't involve recreating data_handler
        if not User.get(unique_id, data_handler):
            User.create(unique_id, users_name, users_email, picture, data_handler)
        login_user(user)
        print("user is authenticated, token is ",token_response.json())
        return("User auth successful")
    
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))
    
    
    
    def post(self):
        """
        Process JSON input for doctor category
        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                payload:
                  type: object
                  properties:
                    conversation:
                      type: object
                      properties:
                        answers:
                          type: object
                          properties:
                            answers:
                              type: object
                              properties:
                                symptoms:
                                  type: string
                                symptoms_duration:
                                  type: string
                                age:
                                  type: string
                                dietary_preferences:
                                  type: string
                                medications:
                                  type: string
                                health_history:
                                  type: string
                                alcohol_consumption:
                                  type: boolean
                                tobacco_use:
                                  type: boolean
                          required:
                            - symptoms
                            - symptoms_duration
                            - age
                            - dietary_preferences
                            - medications
                            - health_history
                            - alcohol_consumption
                            - tobacco_use
                    patient:
                      type: object
                      properties:
                        uuid:
                          type: string
                        email:
                          type: string
                        location:
                          type: object
                          properties:
                            latitude:
                              type: number
                            longitude:
                              type: number
                  required:
                    - conversation
                    - patient
                    - uuid
                    - location
        responses:
            200:
                description: OK
        """
        input_data = request.get_json()
        # Extract the required information from the input_data
        conversation = input_data['payload']['conversation']
        patient = input_data['payload']['patient']
        location = patient['location']
        answers = conversation['answers']['answers']

        # invoke method to get doctor type based on detailed description
        prompt_data = PromptProcessor.create_prompt(answers)

        # Process the data and save it to Firebase
        data_handler.process_data_and_save(patient, answers)

        # Return the response from the OpenAI API
        ##TODO::invoke method to get user current location and top3 nearby doctors/healthcare details
        ##TODO::return  recommeneded results to front end
        return prompt_data, 200


api.add_resource(DoctorCategoryResource, '/doctor-category')


if __name__ == '__main__':
    app.run(ssl_context="adhoc",debug=True)
