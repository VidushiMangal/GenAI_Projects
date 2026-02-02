from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- FUNCTIONS ---------------- #

def enable_lights():
    print("LIGHTBOT: Lights enabled.")

def set_light_color(rgb_hex: str):
    print(f"LIGHTBOT: Lights set to {rgb_hex}.")

def stop_lights():
    print("LIGHTBOT: Lights turned off.")

def print_history(messages):
    for msg in messages:
        role = msg["role"].upper()
        content = msg.get("content")
        if content:
            print(f"{role}: {content}")

# ---------------- TOOLS SCHEMA ---------------- #

tools = [
    {
        "type": "function",
        "function": {
            "name": "enable_lights",
            "description": "Turn on the lights",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_light_color",
            "description": "Set the light color",
            "parameters": {
                "type": "object",
                "properties": {
                    "rgb_hex": {
                        "type": "string",
                        "description": "Hex color like #FF0000"
                    }
                },
                "required": ["rgb_hex"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "stop_lights",
            "description": "Turn off the lights",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

# ---------------- SYSTEM PROMPT ---------------- #

instruction = """
You are a helpful lighting system bot.
Use tools when needed to control the lights.
Do not perform any other tasks.
"""

messages = [{"role": "system", "content": instruction}]

# ---------------- CHAT LOOP ---------------- #

while True:
    user_input = input(
        "What's your wish for lighting system (type exit/quit to exit): "
    ).strip().lower()

    if user_input in ("exit", "quit"):
        print("Exiting lighting system...")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="groq/llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
        tool_choice="auto"   # ✅ AUTO MODE
    )

    msg = response.choices[0].message

    # ---- If model calls tools ----
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments or "{}")

            if name == "enable_lights":
                enable_lights()

            elif name == "set_light_color":
                set_light_color(args["rgb_hex"])

            elif name == "stop_lights":
                stop_lights()

        # Store tool-call message
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": msg.tool_calls
        })
            # ---- If model replies with text ----
    else:
        messages.append({
        "role": "assistant",
        "content": msg.content
    })
    print("ASSISTANT:", msg.content)

print("-" * 60)
