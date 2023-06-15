from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger
import requests
from prompt_processor import PromptProcessor
from data_handler import DataHandler

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'
swagger = Swagger(app)
api = Api(app)

# Create an instance of the DataHandler class
data_handler = DataHandler('https://gptsnackdandies-default-rtdb.firebaseio.com/', 'gptsnackdandies-firebase-adminsdk-7ctws-a01d4f1f29.json')

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
    app.run(debug=True)
