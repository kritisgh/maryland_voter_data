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
            "content": "Give me a statewide summary of this voter data in the year 2024 and some quick facts about the voter data in each county from the year 2024, keep it brief, around 3-4 sentences at the maximum. I just want qualitative reports, no numbers at all and make sure the age ranges are diverse and don't include just older age groups. Give me one standout fact from each county such as age group behavior or voter actions. You are writing like a journalist this voter data."
        },
        {
            "role": "user",
            "content": f"Give me some random qualitative quick hits for each county and give me a statewide summary of this voter data in the year 2024 from this data, make sure the age ranges are diverse and don't include just older age groups. Also give me one standout fact from each county such as age group behavior or voter actions: {text}."
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


