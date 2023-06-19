import os
from flask import Flask, request, redirect
from flask_restful import Api, Resource
from flasgger import Swagger
from ai_engine import OpenAiHelper
from prompt_processor import PromptProcessor
from data_handler import DataHandler
from recommendation_engine import GooglePlaceHelper
import json
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
swagger = Swagger(app)
api = Api(app)

# Create an instance of the DataHandler class
data_handler = DataHandler()
open_ai_helper = OpenAiHelper()


class DoctorCategoryResource(Resource):
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

        prompt_data = PromptProcessor.create_prompt(answers)
        try:
            expert_suggestion = open_ai_helper.find_experts(prompt_data)
            # extract doctor choice
            expert_suggestion = expert_suggestion['choices'][0]['text']
            initial_radius = 1500
            query_count = 0

            # call the find_expert method in the initial radius
            # if status is ZERO_RESULTS, increase the radius by 1000 and try again
            while True:
                query_count += 1
                expert_details = GooglePlaceHelper.find_expert(location['latitude'], location['longitude'], initial_radius, "doctor", expert_suggestion)
                expert_string = expert_details.content.decode('utf-8')
                expert_json = json.loads(expert_string)
                if expert_json['status'] == 'ZERO_RESULTS':
                    initial_radius += 1000
                else:
                    print("Queried google places ",query_count," times")
                    break
        except Exception as e:
            print("Error while generating the expert suggestion",e)
            return expert_suggestion, 500
    
        # Process the data and save it to Firebase
        #TODO: Extract other needed information for the firebase structures
        try:
            data_handler.process_data_and_save(patient, answers, expert_suggestion)
        except Exception as e:
            print("Error while saving the patient's details : ",e)
            
       
        # creating a parsable json object, because the expert_details can't be directly returned
        expert_string = expert_details.content.decode('utf-8')
        expert_json = json.loads(expert_string)
        print(expert_json)
        return expert_json,200
    
@app.route('/')
def redirect_to_apidocs():
    return redirect('/apidocs')

api.add_resource(DoctorCategoryResource, '/doctor-category')


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT", 8080)))
