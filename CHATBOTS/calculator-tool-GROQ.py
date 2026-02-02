from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- FUNCTIONS/TOOLS ---------------- #

def addition(x:int ,y: int):
    return x+y

def subtraction(x:int ,y: int):
    return x-y

def multiplication(x:int ,y: int):
    return x*y

def division(x:int ,y: int):
    if y==0:
        return "Error:Division by 0"
    else:
        return x/y

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
            "name": "addition",
            "description": "Add 2 numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "x":{
                        "type":"integer",
                        "description":"First Number"
                    },
                    "y":{
                        "type":"integer",
                        "description":"Second Number"
                    }
                },
                "required": ["x","y"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "subtraction",
            "description": "perform subtraction",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "integer",
                        "description":"First Number"                        
                    },
                    "y":{
                        "type":"integer",
                        "description":"Second Number"
                    }
                },
                "required": ["x","y"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multiplication",
            "description": "perform multiplication",
            "parameters": {
                "type": "object",
                "properties": {
                    "x":{
                        "type":"integer",
                        "description":"First Number"
                    },
                    "y":{
                        "type":"integer",
                        "description":"Second Number"
                    }
                },
                "required": ["x","y"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"division",
            "description":"divide 2 numbers",
            "parameters":{
                "type":"object",
                "properties":{
                    "x":{
                        "type":"integer",
                        "description":"First Number"
                    },
                    "y":{
                        "type":"integer",
                        "description":"Second Number"
                    }
                },
                "required":["x","y"]
            }
        }
    },
]

# ---------------- SYSTEM PROMPT ---------------- #

instruction = """
You are a helpful mathematical tool.
"""

messages = [{"role": "system", "content": instruction}]

# ---------------- CHAT LOOP ---------------- #
while True:
    first_number = int(input("Enter first number:"))
    second_number = int(input("Enter second number:"))
    operation=input("which operation youwant to perform (addition/subtraction/multiplication/division or quit/exit) ::: ")
    
    if operation in ("exit", "quit"):
        print("Exiting ...")
        break

    messages.append({"role": "user", "content": f"{operation} on {first_number} and {second_number}"})

    response = client.chat.completions.create(
        model="groq/llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
        tool_choice="auto"   # AUTO MODE
    )

    msg = response.choices[0].message

    # ---- If model calls tools ----
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments or "{}")

            if name == "addition":
                result=addition(args["x"],args["y"])

            elif name == "subtraction":
                result=subtraction(args["x"],args["y"])

            elif name == "multiplication":
                result=multiplication(args["x"],args["y"])
            
            elif name=="division":
                result=division(args["x"],args["y"])

        # Store tool-call message
        messages.append({"role": "assistant", "content": None, "tool_calls": msg.tool_calls  })
            # ---- If model replies with text ----
    else:
        messages.append({
        "role": "assistant",
        "content": msg.content
    })
    print("ASSISTANT:", msg.content)

print("-" * 60)
