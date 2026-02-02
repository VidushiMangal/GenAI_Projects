from langchain_groq import ChatGroq
# llm = ChatGroq(
#     model="groq/compound-mini",  
#           temperature=0
# )
# response = llm.invoke("Explain LangChain in simple words")
# print(response.content)

def get_completion(prompt, model="groq/compound-mini"):
    llm = ChatGroq(
        model=model,
        temperature=0, # this is the degree of randomness of the model's output
    )
    response=llm.invoke(prompt)
    return (response.content)

text = """
You should express what you want a model to do by
providing instructions that are as clear and
specific as you can possibly make them.
This will guide the model towards the desired output,
and reduce the chances of receiving irrelevant
or incorrect responses. Don't confuse writing a
clear prompt with writing a short prompt.
In many cases, longer prompts provide more clarity
and context for the model, which can lead to
more detailed and relevant outputs.
"""

# prompt = f"""
# Summarize the text delimited by triple backticks into a single sentence.
# ```{text}```
# """
prompt = f"""
provide 3 book title along with author name, publisher, year of publishing /
in tabular format"""

response = get_completion(prompt)
print(response)