import streamlit as st
import pandas as pd

# if "simple" not in st.session_state:
#   with open("example.txt") as f:
#     simple = f.read()
#   st.session_state.simple = simple
# simple = st.session_state.simple
with open("example.txt") as f:
  simple = f.read()

# Set up the Streamlit app layout
st.title("Chat with Database")
st.subheader("Simple Ideas Business Question")

st.divider()
questions = ["* "+sq for sq in simple.split('\n')]
mark_questions = '\n'.join(questions)
st.markdown(mark_questions)
st.rerun()