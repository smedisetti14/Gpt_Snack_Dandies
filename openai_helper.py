import os
import openai

openai.api_key = "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"

# make a request to openai
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
    presence_penalty=0.0
)

# print the response
print(response)