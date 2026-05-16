# travel-itinerary

Problem statement - 

Use an LLM with Pydantic in Python to generate a structured travel itinerary in JSON with fields. No other input, take a random source city and destination city, and create this using the models’ own knowledge. The aim is to understand how to use Pydantic to create structured output adhering to a fixed schema:
destination: str
trip_duration_days: int
budget_category: str
top_attractions: list[str]
daily_plan: list[{day: int, activities: list[str]}].
