import os
import json
import google.generativeai as genai

# ---------------- GEMINI SETUP ---------------- #

#genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
genai.configure(api_key="AIzaSyBvL0adClZf7KwCgLyd0RN9wQg8lkDC1hY")

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",  # free-tier friendly
    tools=[
        {
            "function_declarations": [
                {
                    "name": "addition",
                    "description": "Add 2 numbers",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "integer"},
                            "y": {"type": "integer"}
                        },
                        "required": ["x", "y"]
                    }
                },
                {
                    "name": "subtraction",
                    "description": "perform subtraction",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "integer"},
                            "y": {"type": "integer"}
                        },
                        "required": ["x", "y"]
                    }
                },
                {
                    "name": "multiplication",
                    "description": "perform multiplication",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "integer"},
                            "y": {"type": "integer"}
                        },
                        "required": ["x", "y"]
                    }
                },
                {
                    "name": "division",
                    "description": "divide 2 numbers",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "integer"},
                            "y": {"type": "integer"}
                        },
                        "required": ["x", "y"]
                    }
                }
            ]
        }
    ]
)

# ---------------- FUNCTIONS ---------------- #

def addition(x, y):
    return x + y

def subtraction(x, y):
    return x - y

def multiplication(x, y):
    return x * y

def division(x, y):
    if y == 0:
        return "Error: Division by 0"
    return x / y

# ---------------- CHAT LOOP ---------------- #

chat = model.start_chat()

while True:
    first_number = int(input("Enter first number: "))
    second_number = int(input("Enter second number: "))
    operation = input(
        "which operation you want to perform "
        "(addition/subtraction/multiplication/division or quit/exit): "
    )

    if operation in ("exit", "quit"):
        print("Exiting ...")
        break

    prompt = f"{operation} on {first_number} and {second_number}"

    response = chat.send_message(prompt)

    part = response.candidates[0].content.parts[0]

    # ---- Tool call handling ----
    if part.function_call:
        name = part.function_call.name
        args = part.function_call.args

        if name == "addition":
            result = addition(args["x"], args["y"])
        elif name == "subtraction":
            result = subtraction(args["x"], args["y"])
        elif name == "multiplication":
            result = multiplication(args["x"], args["y"])
        elif name == "division":
            result = division(args["x"], args["y"])

        print("ASSISTANT:", result)

    else:
        print("ASSISTANT:", part.text)

print("-" * 60)
