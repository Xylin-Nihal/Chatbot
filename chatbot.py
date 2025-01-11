from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
from streamlit_chat import message


# Set up the Streamlit page
st.set_page_config(page_title="Xylin's bot", page_icon="💬")
st.title("Xylin's bot")
st.markdown("try to talk to me")
prompt=ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. your name is Xylin. "),
    ("human", "{input}")
])

llm=Ollama(model="llama2")
output_parser=StrOutputParser()

chain=prompt|llm|output_parser

# Define session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Add a container for the chat
chat_container = st.container()

# Input box for user messages
with st.form(key="chat_form"):
    user_input = st.text_input("Type your message...", key="user_input", placeholder="Message...", label_visibility="hidden")
    submit_button = st.form_submit_button(label="Send")

# Append user message to chat if the form is submitted
if submit_button and user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Placeholder response from the bot
    bot_response = f"You said: {user_input}"  # Replace with AI logic
    st.session_state["messages"].append({"role": "bot", "content": chain.invoke({"input": user_input})})

# Render chat messages in order and allow customization of icons
with chat_container:
    for message_data in st.session_state["messages"]:
        if message_data["role"] == "user":
            message(
                message_data["content"], 
                is_user=True, 
                key=f"user_{message_data['content']}"
                ``
            )
        else:
            message(
                message_data["content"], 
                is_user=False, 
                key=f"bot_{message_data['content']}" 
                  
            )

if submit_button:
    st.rerun()
