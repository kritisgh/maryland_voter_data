import os
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))


def extract_info(text):
    completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "system",
            "content": "With the data I provided, generate 2-3 randomized facts about general voter data in the years 2020-2024 on the given data. For years 2020-2024, find some quick but notable trends. Keep it within 2-3 sentences and keep randomizing the facts every time I prompt you. I also want you to create a small meticulous paragraph format narrative for every county with the 2024 election voter data. Try not to keep the facts limited to ages like 18-24, I want diverse facts. An example of this would be Allegany County: The 2024 voter data from Allegany County shows a strong presence of Republican voters, with 11,152 registered Republicans, compared to 983 registered Democrats. In addition to the small paragraph, give me 2-3 voter facts for each county in the 2024 election cycle. Please advise 'UNA' stands for unaffiliated, if there is a time where UNA comes in your response, I want you to convert that into unaffiliated. Note that I do not want any '*' or '**' in the response."
        },
        {
            "role": "user",
            "content": f"Give me some random quick hits about this data: {text}."
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


