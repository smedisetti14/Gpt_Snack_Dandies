class PromptProcessor():
    def create_prompt(description):
        # Extract the required information from the description
        age = description.get('age')
        alcohol_consumption = description.get('alcohol_consumption')
        dietary_preferences = description.get('dietary_preferences')
        health_history = description.get('health_history')
        medications = description.get('medications')
        symptoms = description.get('symptoms')
        symptoms_duration = description.get('symptoms_duration')
        tobacco_use = description.get('tobacco_use')
        
         #if tobacco_use is false, replace the value with do otherwise replace it with don't
        tobacco_use = "don't" if tobacco_use == 'false' else "do"

        #if alcohol_consumption is false, replace the value with do otherwise replace it with don't
        alcohol_consumption = "don't" if alcohol_consumption == 'false' else "do"

        placeholder_string = '''Hello, I'm suffering from the following symptoms: {symptoms}, 
        from the last {symptoms_duration} days. 
        My age is {age} and my diet is {dietary_preferences}. 
        I {tobacco_use} have smoking habits. I {alcohol_consumption} have drinking habits. 
        My previous health problems include: {health_history}.
        I've been taking the {medications} medicines regularly. 
        Please suggest a doctor for me. Please provide one word answer.'''
        
        # Replace the placeholders with the extracted information
        placeholder_string = placeholder_string.format(symptoms=symptoms, 
                                                       symptoms_duration=symptoms_duration,
                                                       age=age,
                                                       dietary_preferences=dietary_preferences,
                                                       tobacco_use=tobacco_use,
                                                       alcohol_consumption=alcohol_consumption,
                                                       health_history=health_history,
                                                       medications=medications)
        return placeholder_string
