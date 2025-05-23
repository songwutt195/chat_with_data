import streamlit as st
import google.generativeai as genai
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

if "model" not in st.session_state:
  key = st.secrets['gemini_api_key']
  # key = 'AIzaSyBYl0fF5LxGSI1DJ6i7GEF9oBzEO_UXu6I'
  genai.configure(api_key=key)
  st.session_state.model = genai.GenerativeModel('gemini-2.0-flash-lite')
model = st.session_state.model

if "bq_client" not in st.session_state:
  service_account_info = {
    "type": "service_account",
    "project_id": st.secrets['service_project_id'],
    "private_key_id": st.secrets['service_private_key_id'],
    "private_key": st.secrets['service_private_key'],
    "client_email": st.secrets['service_client_email'],
    "client_id": st.secrets['service_client_id'],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": st.secrets['service_client_x509_cert_url'],
    "universe_domain": "googleapis.com"
  }
  # service_account_info = {
  #   "type": "service_account",
  #   "project_id": "gen-lang-client-0545696597",
  #   "private_key_id": "5ca32a1f2efee66ea5991cbdd243fa80b25ed024",
  #   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCuVgdj02UZ2KRq\nKygetQFOJ9ORrF9oHnnET4Lh+iN54hcWN800dOcUnyfWJnyiNMT8h9XxfIAzWQcK\nmWLtJTWV7IwowtdEO21YJqNSC84Lu9B7a6FzMGVdb2NCFxulifbo5MJ+F1jy4z0n\nIzQRCltRZKLwDbiHnnGodJZOuuEL962MZUY4ODFQexnbSLvWWXQIMCtrFXAtAQ43\nNCAYEsUyNznu45jhR+AdKnq3Hp3lPHtBQzIjVxyUn30MWPHEzRTyXXZx58URLuXV\ngBCE+O1EmiCa2SuAcs7v7Y8ppKdYfpbTVKMIsi9YxOYUMG3Ahb+C5/cZCzP6aNAY\nDWEfxu3fAgMBAAECggEANkAbKJtd+L8L2uX3JCcbcuC927USM2pYZhiAGCYo6ALN\nQGK4/rvqNOaaFPABFNDrA9KZZv5hPplTsZ6txDIyDKeBriWDq336ttW/OQbnZYta\ngy2pHhlPUdYZwzVBqy/Vn/+f7nEBgwPnwcgYqbzZUejJM35xj/JkWBF/vJw27+vt\nNrTIQT/MWE3/0JNA4Txg3MAbxGUy8loYXc3jWyxFcm9o/pAn5GhkekICp8k8Jytp\njbz8B5piFP0Qb0cGOsND6SPIZHCpKZL+MdgMwMGHBjigJF3uX396cbNn2lMEmUQ9\nc4NTgioxXbsm6aCz//MN2dfTx5wVtNbiq7iRUmuwoQKBgQDkqlzGxmKFkoVeKotB\nbDJYlkCwSJT+vBaimwtnRxdHeEHsLd1MHCdJgD/YPRsKk2hm/JP7kJGjCLcacfwA\nzze6l3q1/Or28WO397x4Zbv36+YfkpXFHlgOfTBJnmJkGBUvi+0NNdsPVonfXXpb\n2KIoNAL2MBur5khEs7d3TsLJGQKBgQDDLRLHa+i7IV+ANVvTLmlCPm6bvYprEedZ\nNX/y3zJdIXUFrTojCalaABOrqvIgwi4/r61O3jU/grrZ5lBRxLwOm1w+KDOwzFDx\nmk19pppg4E1LDkM3BDZLClpWN6WX4OAEff/JXxU94pdbG72BfcFTHE+n9+zhA/oW\n0eFPh/81twKBgQCaf2DgDPpUNYNW9HfSZEBACoT6lo/U7VB93TP/O9FGwMIJyZNT\n8VG6H6UDfYXfx2kq7E0wE6XS+fh9LbaO9XM5509J1vEKmF4/1mrJDjPKduCtRGVd\nIfttDriphRIFfyARWAF6g4DXBClzeb1KgTxO3ZWCsU6A/r6lbKfxPI3vQQKBgH+o\nDn1S7iDfPiiMPegNlhkW3p+MxGkth6TIokxHghh51qGE4N6j5hmQrUz9/WpBt6A+\nFlvcaPWGWxJEWspwpBPlt9qLzutXZ6Xup7qEarrsWoG57WqhnaVNOzLjKLMDCWLG\nyrN6NlmIyDh2F2gHyZfDj7IsLcorILsmQXkUWW9XAoGBAL9eY51LVcm31lWl0ER7\nALdoLz8WmnDc/OGq3KjaWp52iXDkW4EqKfAkeJMX0rcwvvstBu0qWvM3nU0SE+4H\nW6VufwAWnq61x2suW+RVDH2cniNapmjL9gcfXLK665ICiCaeF3k+oD7TdlbJuiVd\nrYWbroUa89n4W8dD8IgQBZf9\n-----END PRIVATE KEY-----\n",
  #   "client_email": "test-678@gen-lang-client-0545696597.iam.gserviceaccount.com",
  #   "client_id": "116945275583303606224",
  #   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  #   "token_uri": "https://oauth2.googleapis.com/token",
  #   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  #   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test-678%40gen-lang-client-0545696597.iam.gserviceaccount.com",
  #   "universe_domain": "googleapis.com"
  # }

  credentials = service_account.Credentials.from_service_account_info(service_account_info)
  st.session_state.bq_client = bigquery.Client(credentials=credentials)
bq_client = st.session_state.bq_client

# if "extract_prompt" not in st.session_state:
#   with open("prompt_extract.txt") as f:
#     extract_prompt = f.read()
#   st.session_state.extract_prompt = extract_prompt
# extract_prompt = st.session_state.extract_prompt
with open("prompt_extract.txt") as f:
  extract_prompt = f.read()

# if "query_prompt" not in st.session_state:
#   with open("prompt_query.txt") as f:
#     query_prompt = f.read()
#   st.session_state.query_prompt = query_prompt
# query_prompt = st.session_state.query_prompt
with open("prompt_query.txt") as f:
  query_prompt = f.read()

# if "explain_prompt" not in st.session_state:
#   with open("prompt_explain.txt") as f:
#     explain_prompt = f.read()
#   st.session_state.explain_prompt = explain_prompt
# explain_prompt = st.session_state.explain_prompt
with open("prompt_explain.txt") as f:
  explain_prompt = f.read()

# if "error_prompt" not in st.session_state:
#   with open("prompt_error.txt") as f:
#     error_prompt = f.read()
#   st.session_state.error_prompt = error_prompt
# error_prompt = st.session_state.error_prompt
with open("prompt_error.txt") as f:
  error_prompt = f.read()
 
if "history" not in st.session_state:
  st.session_state.history = []

def generate_answer(question):
  try:
    response = model.generate_content(extract_prompt.format(question=question))
    response_text = response.text.strip()
    steps = response_text.split('**Analysis Steps:**\n\n')[-1]
    
    response = model.generate_content(query_prompt.format(question=question,
                                                          steps=steps))
    response_text = response.text.strip()
    query = response_text.replace('```sql','').replace('```','')
    
    df = bq_client.query(query).to_dataframe()
    results = df.to_string()
    
    response = model.generate_content(explain_prompt.format(question=question,
                                                            steps=steps,
                                                            results=results))
    answer = response.text.strip()
    return answer
  except Exception as e:
    answer = model.generate_content(error_prompt.format(e=e, question=question))
    return answer

# Set up the Streamlit app layout
st.title("Chat with Database")

col1, col2 = st.columns([0.8,0.2])
col1.subheader("Conversation and Table Augmented Generation")
if col2.button("New Chat"):
  st.session_state.history = []

for message in st.session_state.history:
  with st.chat_message(message['role']):
    st.markdown(message['text'])
        
if prompt := st.chat_input("Start with \"What is yesterday total sale?\""):
  message = {'role':'user','text':prompt}
  st.session_state.history.append(message)
  st.chat_message('user').markdown(prompt)
  answer = generate_answer(prompt)
  message = {'role':'assistant','text':answer}
  st.session_state.history.append(message)
  st.chat_message('assistant').markdown(answer)

st.rerun()