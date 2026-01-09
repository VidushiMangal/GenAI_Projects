import streamlit as st
from langchain_groq import ChatGroq

def get_completion_from_messages(messages):
    llm = ChatGroq(
        model="groq/compound-mini",
        temperature=0
    )
    response = llm.invoke(messages)
    return response.content

st.set_page_config(page_title="Burger OrderBot ")
st.title(" Burger OrderBot")
st.image(
    "https://images.unsplash.com/photo-1550547660-d9450f859349",
    width=300
)

if "context" not in st.session_state:
    st.session_state.context = [
        {
    'role': 'system',
    'content': """
    You are BurgerBot, an automated service to collect orders for a burger parlour. \
    You first greet the customer, then collect the burger order, \
    and then ask if it's dine-in, takeaway, or delivery. \
    You wait to collect the entire order, then summarize it and check one final \
    time if the customer wants to add anything else. \
    If it's a delivery, you ask for the delivery address. \
    Finally, you collect the payment. \
    Make sure to clarify all options, add-ons, and sizes to uniquely \
    identify each item from the menu. \
    You respond in a short, friendly, conversational style. \
    The menu includes \
    Veg Burger 6.50, 5.50, 4.50 \
    Cheese Burger 7.50, 6.50, 5.50 \
    Chicken Burger 8.50, 7.50, 6.50 \
    Double Patty Burger 10.50, 9.50, 8.50 \
    French Fries 4.00, 3.00 \
    Onion Rings 4.50 \
    Add-ons: \
    extra cheese 1.50, \
    lettuce 0.50 \
    tomato 0.50 \
    jalapenos 1.00 \
    fried egg 1.50 \
    Sauces: \
    mayonnaise 0.50 \
    ketchup 0.50 \
    BBQ sauce 1.00 \
    Drinks: \
    cola 3.00, 2.00, 1.50 \
    orange soda 3.00, 2.00, 1.50 \
    bottled water 2.50 \
    """
           } 
    ]

for msg in st.session_state.context:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

user_input = st.chat_input("Hi... Which would you like to eat today....")

if user_input:
    # Add user message
    st.session_state.context.append(
        {"role": "user", "content": user_input}
    )

    # Get assistant response
    response = get_completion_from_messages(st.session_state.context)

    # Add assistant response
    st.session_state.context.append(
        {"role": "assistant", "content": response}
    )

    st.rerun()
