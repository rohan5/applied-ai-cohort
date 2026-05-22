from pydantic import BaseModel
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()


# -----------------------------
# Pydantic Models
# -----------------------------

class DailyPlan(BaseModel):
    day: int
    activities: List[str]


class TravelItinerary(BaseModel):
    destination: str
    trip_duration_days: int
    budget_category: str
    top_attractions: List[str]
    daily_plan: List[DailyPlan]


# -----------------------------
# Prompt
# -----------------------------

prompt = """
Generate a travel itinerary in JSON format.

Choose:
- a random source city
- a random destination city

Return ONLY valid JSON matching this schema:

{
  "destination": "string",
  "trip_duration_days": number,
  "budget_category": "Budget | Mid-range | Luxury",
  "top_attractions": ["attraction1", "attraction2"],
  "daily_plan": [
    {
      "day": number,
      "activities": ["activity1", "activity2"]
    }
  ]
}
"""


# -----------------------------
# Call LLM
# -----------------------------

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.8
)

# Raw text response from model
content = response.choices[0].message.content

print("\nRaw LLM Response:\n")
print(content)


# -----------------------------
# Convert JSON -> Pydantic
# -----------------------------

content = content.replace("```json", "").replace("```", "").strip()

itinerary_dict = json.loads(content)

itinerary = TravelItinerary.model_validate(itinerary_dict)


# -----------------------------
# Output Structured Data
# -----------------------------

print("\nValidated Pydantic Object:\n")
print(itinerary)


print("\nDestination:", itinerary.destination)

print("\nDaily Plan:")

for day in itinerary.daily_plan:
    print(f"\nDay {day.day}")

    for activity in day.activities:
        print("-", activity)