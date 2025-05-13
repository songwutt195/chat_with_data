import streamlit as st
import google.generativeai as genai
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

# Set up the Streamlit app layout
st.title("Chat with Database")

st.subheader("Conversation and Table Augmented Generation")