from openai import OpenAI
from typing import List
from pydantic import BaseModel

client = OpenAI()

print("Hello world!")

class DailyPlan(BaseModel):
    day: int
    activities: List[str]

class TravelItinerary(BaseModel):
    destination: str
    trip_duration: int
    budget_category: str
    top_attractions: List[str]
    daily_plan: List[DailyPlan]

prompt = "Take a random source and destination city. And create an travel itinerary for me in JSON format"

response = client.responses.parse(
    model="gpt-5.4-mini",
    input=prompt,
    text_format=TravelItinerary
)

itinerary = response.output_parsed

print(itinerary)

print("\n Destination : ", itinerary.destination)

print("\n Top attractions: ")

for attr in itinerary.top_attractions:
    print("\n - ", attr)

print("\n Daily Plan")
for day in itinerary.daily_plan:
    print(day)
    for activity in day.activities:
        print("\n - ", activity)