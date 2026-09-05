import json
import streamlit as st
from google import genai
from google.genai import types


MODEL = "gemini-3.6-flash"


def get_client():
    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Add it to .streamlit/secrets.toml"
        )

    return genai.Client(api_key=api_key)


def generate_answer(question, history=None):
    history = history or []

    client = get_client()

    previous = "\n".join(
        f"{i + 1}. {item}"
        for i, item in enumerate(history[-8:])
    )

    if not previous:
        previous = "No previous questions. This is the beginning."

    prompt = f"""
You are the AI engine for a game called THE RABBIT HOLE.

The player asks a question.

Your job is to:
1. Answer the question accurately.
2. Explain the answer clearly and interestingly.
3. Give exactly three questions that lead deeper into the answer.
4. Make each follow-up genuinely connected to the answer.
5. Make the three choices different from one another.
6. Avoid repeating previous questions.
7. Never invent facts.
8. If something is uncertain, say so.
9. Keep the answer understandable for a curious teenager.
10. Prefer surprising connections when they are actually relevant.

PREVIOUS JOURNEY:
{previous}

CURRENT QUESTION:
{question}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "answer": "A clear and accurate answer to the question.",
    "hook": "One short sentence that makes the player curious.",
    "choices": [
        {{
            "category": "SCIENCE",
            "title": "A complete deeper question?",
            "description": "Why this is an interesting next step."
        }},
        {{
            "category": "HISTORY",
            "title": "Another complete deeper question?",
            "description": "Why this is an interesting next step."
        }},
        {{
            "category": "SURPRISING CONNECTION",
            "title": "A surprising connected question?",
            "description": "Why this is an interesting next step."
        }}
    ]
}}

There MUST be exactly three choices.
Every choice title MUST be a complete question.
"""


    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        if response is None or not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        result = json.loads(response.text)

    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Gemini returned invalid JSON: {error}"
        )

    except Exception as error:
        raise RuntimeError(
            f"Gemini request failed: {error}"
        )

    if not isinstance(result, dict):
        raise RuntimeError("Gemini returned an invalid response.")

    answer = result.get("answer")
    hook = result.get("hook")
    choices = result.get("choices")

    if not answer:
        raise RuntimeError("Gemini response did not contain an answer.")

    if not hook:
        hook = "There is probably another layer hiding underneath this."

    if not isinstance(choices, list) or len(choices) < 3:
        raise RuntimeError(
            "Gemini did not return three rabbit-hole choices."
        )

    clean_choices = []

    for choice in choices[:3]:
        if not isinstance(choice, dict):
            continue

        title = choice.get("title")
        description = choice.get("description")
        category = choice.get("category", "RABBIT HOLE")

        if not title:
            continue

        clean_choices.append({
            "category": category,
            "title": title,
            "description": description or "Follow this connection deeper."
        })

    if len(clean_choices) != 3:
        raise RuntimeError(
            "Gemini returned fewer than three usable choices."
        )

    return {
        "answer": answer,
        "hook": hook,
        "choices": clean_choices
    }


SURPRISES = [
    {
        "from": "One question",
        "to": "A hidden connection",
        "connection": "The rabbit hole just crossed into another idea."
    },
    {
        "from": "Something familiar",
        "to": "Something unexpected",
        "connection": "Two ideas that seem unrelated can actually share the same underlying principle."
    },
    {
        "from": "Your question",
        "to": "A bigger mystery",
        "connection": "The deeper you look, the more interesting the original question becomes."
    },
    {
        "from": "One field",
        "to": "Another field",
        "connection": "This is where different areas of knowledge start to overlap."
    },
    {
        "from": "A simple answer",
        "to": "A complicated world",
        "connection": "There is much more underneath the first explanation."
    },
]


def get_surprise(depth=1):
    return SURPRISES[(depth - 1) % len(SURPRISES)]