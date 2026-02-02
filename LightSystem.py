from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def enable_lights():
    print("LIGHTBOT: Lights enabled.")

def set_light_color(rgb_hex: str):
    print(f"LIGHTBOT: Lights set to {rgb_hex}.")

def stop_lights():
    print("LIGHTBOT: Lights turned off.")

def print_history(messages):
    for msg in messages:
        print(f"{msg['role'].upper()}: {msg['content']}")

light_controls = [enable_lights, set_light_color, stop_lights]
instruction = """
  You are a helpful lighting system bot. You can turn
  lights on and off, and you can set the color. Do not perform any
  other tasks.
"""

messages=[{"role":"system","content":instruction}]

while True:
    user_input = input(
        "What's your wish for lighting system (type exit/quit to exit): ")
    if user_input in ("exit", "quit"):
        print("Exiting lighting system...")
        break

    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(model="groq/compound-mini",messages=messages,)
    assistant_reply=response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_reply})

    print_history(messages)
