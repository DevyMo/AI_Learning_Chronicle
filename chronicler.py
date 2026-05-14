import os
import json
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_DIR = Path(__file__).parent
INBOX_DIR = BASE_DIR / "inbox"
PROCESSED_DIR = BASE_DIR / "processed"
DRAFTS_DIR = BASE_DIR / "drafts"
MEMORY_DIR = BASE_DIR / "memory"

MODEL = "gpt-5.4-mini"


def read_markdown_files():
    files = sorted(INBOX_DIR.glob("*.md"))
    notes = []

    for file in files:
        notes.append({
            "filename": file.name,
            "content": file.read_text(encoding="utf-8")
        })

    return notes


def summarize_note(note):
    prompt = f"""
You are helping create a personal AI learning journal.

Summarize the following note into structured JSON.

Filename: {note["filename"]}

Note:
{note["content"]}
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "learning_note_summary",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "title": {"type": "string"},
                        "main_idea": {"type": "string"},
                        "what_i_learned": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "tools_or_concepts": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "real_world_use_case": {"type": "string"},
                        "family_friendly_explanation": {"type": "string"},
                        "next_step": {"type": "string"}
                    },
                    "required": [
                        "title",
                        "main_idea",
                        "what_i_learned",
                        "tools_or_concepts",
                        "real_world_use_case",
                        "family_friendly_explanation",
                        "next_step"
                    ]
                }
            }
        }
    )

    return json.loads(response.output_text)


def save_summary(filename, summary):
    output_file = PROCESSED_DIR / filename.replace(".md", ".json")
    output_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return output_file


def load_summaries():
    summaries = []

    for file in sorted(PROCESSED_DIR.glob("*.json")):
        summaries.append(json.loads(file.read_text(encoding="utf-8")))

    return summaries


def load_memory():
    memory_file = MEMORY_DIR / "timeline.json"

    if not memory_file.exists():
        return []

    return json.loads(memory_file.read_text(encoding="utf-8"))


def save_memory(memory):
    memory_file = MEMORY_DIR / "timeline.json"

    memory_file.write_text(
        json.dumps(memory, indent=2),
        encoding="utf-8"
    )


def generate_digest(summaries):
    prompt = f"""
You are creating a warm, family-friendly weekly update about my AI learning journey.

Use these structured summaries:

{json.dumps(summaries, indent=2)}

Create a polished markdown article with this structure:

# What I Learned About AI This Week

## Big Idea

## What I Explored

## Simple Explanation

## Why This Matters

## Real-World Use Case

## What I’m Trying Next
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt
    )

    return response.output_text


def extract_learning_snapshot(summaries):
    prompt = f"""
You are analyzing my AI learning journey.

From these summaries, extract:

- major themes
- skills gained
- projects worked on
- likely next focus areas

Return ONLY valid JSON.

Summaries:
{json.dumps(summaries, indent=2)}
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "learning_snapshot",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "themes": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "skills_gained": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "projects": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "next_focus": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": [
                        "themes",
                        "skills_gained",
                        "projects",
                        "next_focus"
                    ]
                }
            }
        }
    )

    return json.loads(response.output_text)


def save_digest(digest):
    today = date.today().isoformat()
    output_file = DRAFTS_DIR / f"weekly-digest-{today}.md"
    output_file.write_text(digest, encoding="utf-8")
    return output_file


def main():
    notes = read_markdown_files()

    if not notes:
        print("No markdown files found in inbox.")
        return

    print(f"Found {len(notes)} note(s).")

    for note in notes:
        print(f"Summarizing {note['filename']}...")
        summary = summarize_note(note)
        save_summary(note["filename"], summary)

    summaries = load_summaries()

    print("Updating memory...")
    
    memory = load_memory()

    snapshot = extract_learning_snapshot(summaries)

    memory.append({
        "date": date.today().isoformat(),
        **snapshot
    })

    save_memory(memory)

    print("Generating weekly digest...")
    digest = generate_digest(summaries)
    digest_file = save_digest(digest)

    print(f"Done. Draft saved to: {digest_file}")


if __name__ == "__main__":
    main()