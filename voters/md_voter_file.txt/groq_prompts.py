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
            "content": "Go through this Maryland Voter Detail from the election years 2020 and 2024 text I gave you, give me very brief 1-2 random facts about each county and try to diversify the age ranges as well. These facts should be very quick digestable information for the reader to read. Please advise 'UNA' stands for unaffiliated and 'OTH' stands for other. You should sound like a news reporter when giving the results. Note that I do not want any '*' or '**' in the response."
        },
        {
            "role": "user",
            "content": f"Give me some random quick hits for each county about this data: {text}."
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
    counties = open("md_voter_details.txt").read().splitlines()
    all_reports = process_batches(counties, batch_size=5, wait=1)
    for batch_info in all_reports:
        print(batch_info["groq_report"])
        print()


