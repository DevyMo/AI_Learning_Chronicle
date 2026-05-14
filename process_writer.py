import os
import json
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_DIR = Path(__file__).parent
PROCESSED_DIR = BASE_DIR / "processed"
DRAFTS_DIR = BASE_DIR / "drafts"

MODEL = "gpt-5.4-mini"


def load_summaries():
    summaries = []

    for file in sorted(PROCESSED_DIR.glob("*.json")):
        summaries.append(json.loads(file.read_text(encoding="utf-8")))

    return summaries


def generate_process_guide(summaries):
    prompt = f"""
You are creating a practical step-by-step guide based on my AI learning project.

Use the following structured summaries:

{json.dumps(summaries, indent=2)}

Create a markdown guide that someone else could follow to repeat what I did.

The guide should be actionable and beginner-friendly.

Structure it like this:

# How I Built My First AI Learning Chronicle

## What This Project Does

## Tools and Accounts Needed

## Folder Structure

## Step-by-Step Setup

## How the Workflow Works

## What Each File Does

## How to Run It

## What Output to Expect

## Common Issues and Fixes

## What I Learned

## Next Improvements

Requirements:
- write clearly
- avoid hype
- explain technical terms simply
- include concrete steps
- include command examples where helpful
- make it useful for a family member or beginner who wants to understand or repeat the project
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt
    )

    return response.output_text


def save_process_guide(guide):
    today = date.today().isoformat()
    output_file = DRAFTS_DIR / f"step-by-step-guide-{today}.md"
    output_file.write_text(guide, encoding="utf-8")
    return output_file


def main():
    summaries = load_summaries()

    if not summaries:
        print("No JSON summaries found in processed/. Run chronicler.py first.")
        return

    print(f"Loaded {len(summaries)} summaries.")
    print("Generating step-by-step guide...")

    guide = generate_process_guide(summaries)
    output_file = save_process_guide(guide)

    print(f"Done. Guide saved to: {output_file}")


if __name__ == "__main__":
    main()