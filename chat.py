import streamlit as st
import google.generativeai as genai
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

# Set up the Streamlit app layout
st.title("Chat with Database")

col1, col2 = st.columns([0.8,0.2])
col1.subheader("Conversation and Table Augmented Generation")
if col2.button("New Chat"):
  st.session_state.history = []

for message in st.session_state.history:
  with st.chat_message(message['role']):
    st.markdown(message['text'])
        
if prompt := st.chat_input("ask here"):
  message = {'role':'user','text':prompt}
  st.session_state.history.append(message)
  st.chat_message('user').markdown(prompt)
  answer = generate_answer(prompt)
  message = {'role':'assistant','text':answer}
  st.session_state.history.append(message)
  st.chat_message('assistant').markdown(answer)

st.rerun()