from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger
import requests
app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'
swagger = Swagger(app)
api = Api(app)
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
                userDetails:
                  type: object
                  properties:
                    userid:
                      type: integer
                    username:
                      type: string
                    userphone:
                      type: integer
                  required:
                    - userid
                    - username
                    - userphone
                locationDetails:
                  type: object
                  properties:
                    latitude:
                      type: number
                    longitude:
                      type: number
                    accuracy:
                      type: number
                    timestamp:
                      type: number
                  required:
                    - latitude
                    - longitude
                    - accuracy
                    - timestamp
                description:
                  type: object
                  properties:
                    Question1:
                      type: string
                    Question2:
                      type: string
                  required:
                    - Question1
                    - Question2
            description: JSON input for doctor category
        responses:
            200:
                description: OK
        """
        input_data = request.get_json()
        # Extract the required information from the input_data
        userDetails = input_data.get('userDetails')
        locationDetails = input_data.get('locationDetails')
        description = input_data.get('description')
        # Process the extracted information as needed
        # ...
        # Return the response from the OpenAI API
        ##TODO::invoke method to get doctor type based on detailed description
        ##TODO::invoke method to save information in FireBASE
        ##TODO::invoke method to get user current location and top3 nearby doctors/healthcare details
        ##TODO::return  recommeneded results to front end
        return description, 200
api.add_resource(DoctorCategoryResource, '/doctor-category')
##TODO::write a logic to call OPEN API to get the response of doctor type based on detailed description
def get_suggested_doctor(symptoms):
    url = 'https://symptomchecker.nlm.nih.gov/symptoms/services/symptoms'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'symp': symptoms}
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    # Extract the suggested doctor or healthcare provider from the response
    suggested_doctor = response_data['doctor']
    return suggested_doctor
# Example usage
symptoms = "Pain or aching in more than one joint, Stiffness in more than one joint, Tenderness and swelling in more than one joint, The same symptoms on both sides of the body, Weight loss, Fever, Fatigue or tiredness, Weakness"
##print(suggested_doctor)
if __name__ == '__main__':
    app.run(debug=True)