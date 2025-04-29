import os
import time
from retry import retry
from rich.progress import track
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

@retry(ValueError, tries=2, delay=2)
def extract_info(text):
    completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "system",
            "content": "With the data I provided, generate 2-3 randomized facts about general voter data in the years 2020-2024 on the given data. For years 2020-2024, find some quick but notable trends. Keep it within 2-3 sentences and keep randomizing the facts every time I prompt you. Try not to keep the facts limited to ages like 18-24, I want diverse facts. An example of this would be Allegany County: The 2024 voter data from Allegany County shows a strong presence of Republican voters, with 11,152 registered Republicans, compared to 983 registered Democrats. In addition to the small paragraph, give me 2-3 voter facts for each county in the 2024 election cycle. Please advise 'UNA' stands for unaffiliated. You should sound like a news reporter when giving the results. Note that I do not want any '*' or '**' in the response."
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

def get_batch_list(li, n=10):
    return [li[i : i + n] for i in range(0, len(li), n)]


def process_batches(raw_text_list, batch_size=10, wait=2):
    results = []
    batches = get_batch_list(raw_text_list, batch_size)

    for batch in track(batches, description="Groq batches"):
        prompt_text = "\n".join(batch)
        
        try:
            report = extract_info(prompt_text)
        except ValueError as e:
            print(f"Batch failed after retry: {e!r}")
            report = None
        
        results.append({
            "batch_input": batch,
            "groq_report": report
        })
        
        time.sleep(wait)

    return results

if __name__ == "__main__":
    counties = open("example.txt").read().splitlines()
    all_reports = process_batches(counties, batch_size=5, wait=1)
    for batch_info in all_reports:
        print(batch_info["groq_report"])
        print()


