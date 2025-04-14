import os
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))


def extract_info(text):
    completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "system",
            "content": "Create a two sentence summary of voter data from people that voted in the 2024 election that includes their gender, age bracket, and legislative property."
        },
        {
            "role": "user",
            "content": f"Give me a summary of this voter data: {text}. Make it brief."
        }
    ],
    temperature=0,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)
    return completion.choices[0].message.content

input_txt_path = 'example.txt'
with open(input_txt_path, 'r') as file:
    content = file.read()
print(extract_info(content))


