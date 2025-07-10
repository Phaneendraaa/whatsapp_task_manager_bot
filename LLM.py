import os
from mistralai import Mistral
import json
import re
model = "mistral-medium"

client = Mistral(api_key="z6JUEWBz0GqVQvYNycWr2qINTxbTUtvt")

def ask(promt):
    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": promt,
            },
        ]   
    )

    return chat_response.choices[0].message.content

from datetime import datetime

def extract_json_object(text):
    """
    Extracts the first valid JSON object from a string using bracket matching.
    """
    start = text.find('{')
    if start == -1:
        return None
    
    bracket_count = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            bracket_count += 1
        elif text[i] == '}':
            bracket_count -= 1
            if bracket_count == 0:
                return text[start:i+1]
    return None

def convert_calendar(message):
    curr = datetime.now().isoformat()

    query = (
        f"You are an assistant that extracts Google Calendar event JSON from text messages.\n"
        f"Current time: {curr}\n\n"
        f"From the following message, extract an event in this exact JSON structure:\n\n"
        f"{{\n"
        f"  \"summary\": \"Title of the event\",\n"
        f"  \"description\": \"Optional details\",\n"
        f"  \"start\": {{\n"
        f"    \"dateTime\": \"YYYY-MM-DDTHH:MM:SS+05:30\",\n"
        f"    \"timeZone\": \"Asia/Kolkata\"\n"
        f"  }},\n"
        f"  \"end\": {{\n"
        f"    \"dateTime\": \"YYYY-MM-DDTHH:MM:SS+05:30\",\n"
        f"    \"timeZone\": \"Asia/Kolkata\"\n"
        f"  }},\n"
        f"  \"reminders\": {{\n"
        f"    \"useDefault\": false,\n"
        f"    \"overrides\": [\n"
        f"      {{\"method\": \"popup\", \"minutes\": 30}},\n"
        f"      {{\"method\": \"popup\", \"minutes\": 5}}\n"
        f"    ]\n"
        f"  }}\n"
        f"}}\n\n"
        f"Message: \"{message}\"\n\n"
        f"Return ONLY the JSON strictly and gather important info. like links , venues and explain task  and add it to description. if the user message is not related to any task event or deadline return a json with summary set as \"no\" .strictly Only return a json , no text"
    )

    response = ask(query)

    json_str = extract_json_object(response)
    if not json_str:
        raise ValueError("No valid JSON object found in LLM response:\n" + response)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError("Failed to decode JSON:\n\n" + json_str + "\n\nError: " + str(e))