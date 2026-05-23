import json
from openai import OpenAI

client = OpenAI()

# -----------------------------
# Fake weather tool
# -----------------------------
def get_weather(city: str):
    # In real life this would call a weather API
    fake_weather_db = {
        "Tokyo": {
            "temperature_c": 26.5,
            "condition": "Sunny",
            "humidity": 58,
        },
        "Paris": {
            "temperature_c": 19.2,
            "condition": "Cloudy",
            "humidity": 71,
        },
        "Sydney": {
            "temperature_c": 14.8,
            "condition": "Rainy",
            "humidity": 83,
        },
    }

    return fake_weather_db.get(
        city,
        {
            "temperature_c": 22.0,
            "condition": "Clear",
            "humidity": 60,
        },
    )

# -----------------------------
# Tool definition
# -----------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name",
                    }
                },
                "required": ["city"],
            },
        },
    }
]

# -----------------------------
# Step 1: Ask model
# -----------------------------
response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        {
            "role": "user",
            "content": (
                "Pick a random city using your own knowledge, "
                "call the weather tool, and return the final result."
            ),
        }
    ],
    tools=tools,
    tool_choice="auto",
)

message = response.choices[0].message

# -----------------------------
# Step 2: Execute tool call
# -----------------------------
tool_call = message.tool_calls[0]

tool_name = tool_call.function.name
arguments = json.loads(tool_call.function.arguments)

city = arguments["city"]

tool_result = get_weather(city)

# -----------------------------
# Step 3: Send tool result back
# -----------------------------
final_response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {
            "role": "user",
            "content": (
                "Pick a random city using your own knowledge, "
                "call the weather tool, and return the final result."
            ),
        },
        message,
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result),
        },
    ],
)

# -----------------------------
# Final output
# -----------------------------
print(final_response.choices[0].message.content)