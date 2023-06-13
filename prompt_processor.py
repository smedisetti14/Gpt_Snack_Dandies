class PromptProcessor():
    def create_prompt(description):
        placeholder_string =  '''Hello, I'm suffering from the following symptoms {symptoms} 
        from the last {days} days,
        my diet is {diet_choice}, 
        and I {choice} have smoking/drinking habits,
        I've been taking the {medicine} medicines regularly, please suggest a
        doctor for me, please provide a one word answer'''

        # Extract the required information from the description
        symptoms = description.get('symptoms')
        diet_choice = description.get('diet_choice')
        choice = description.get('choice')
        
         #if choice is false, replace the value with do otherwise replace it with don't
        choice = "don't" if choice == 'false' else "do"

        medicine = description.get('medicine')
        days = description.get('days')
        # Replace the placeholders with the extracted information
        placeholder_string = placeholder_string.format(symptoms=symptoms, 
                                                       days=days,
                                                       diet_choice=diet_choice,
                                                       medicine=medicine,
                                                       choice=choice)
        return placeholder_string
    
    # sample code to call create_prompt and print result
    description = {'symptoms': [
        "Burning sensation during urination",
        "Frequent urge to urinate",
        "Cloudy or bloody urine",
        "Lower abdominal pain"], 'diet_choice': 'Vegetarian', 'choice': 'false', 
        'medicine': ["Ibuprofen", "Paracetamol"], 'days': '10'}
    print(create_prompt(description))