import os
import openai
from dotenv import load_dotenv

#get openai api key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# make a request to openai
try:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt='''Hello, I'm suffering from the following symptoms ['Burning sensation during urination', 'Frequent urge to urinate', 'Cloudy or bloody urine', 'Lower abdominal pain'] 
            from the last 10 days,
            my diet is Vegetarian, 
            and I don't have smoking/drinking habits,
            I've been taking the ['Ibuprofen', 'Paracetamol'] medicines regularly, please suggest a
            doctor for me, please provide a one word answer''',
        temperature=0.3,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0)
    #print(response)
except openai.error.AuthenticationError as e:
    print("OpenAI unknown authentication error")
    print(e.json_body)
    print(e.headers)



