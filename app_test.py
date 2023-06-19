import unittest
import prompt_processor

class sanity_tests(unittest.TestCase):
    def test_create_prompt(self):
        #create a map called description that contains symptoms, diet-choice, choice and medicine keys
        description = {'symptoms': [
        "Burning sensation during urination",
        "Frequent urge to urinate",
        "Cloudy or bloody urine",
        "Lower abdominal pain"], 'diet_choice': 'Vegetarian', 'choice': 'false', 
        'medicine': ["Ibuprofen", "Paracetamol"], 'days': '10'}
        #Call create_prompt and print the result
        #print(prompt_processor.create_prompt(description))
        #self.assertEqual(prompt_processor.create_prompt(description), "What is your name?")