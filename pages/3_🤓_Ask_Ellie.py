import pandas as pd
import openai
import streamlit as st
import warnings

from classes import get_primer, format_question, run_request

# Set up page config
st.set_page_config(page_icon="chat2vis.png", layout="wide", page_title="Ask Ellie")

st.title("💬 Ask Ellie - Your Personal Finance AI")
st.caption("🚀 Powered by OpenAI and Streamlit")

# Sidebar for user credentials and CSV upload
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password")

uploaded_file = st.file_uploader("Upload your financial CSV data:", type="csv")

# Check if the uploaded file is valid
if uploaded_file:
    financial_data = pd.read_csv(uploaded_file)
    st.session_state["financial_data"] = financial_data
    st.write("Financial data uploaded successfully!")
else:
    st.write("Upload your financial data to get insights from Ellie!")
    financial_data = None

if financial_data is not None:
    st.write("Generating primers for the financial data...")
    primers = get_primer(financial_data.copy())
    
    if primers is None:
        st.error("Unable to generate primers for the provided financial data.")
        st.stop()
    else:
        primer_desc, primer_code = primers
        
        st.write("Primers generated successfully.")

    # Greet the user with the primer description
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": f"Hi! I've noticed your data has the following structure: {primer_desc}. How can I assist you?"}]
else:
    primer_desc, primer_code = None, None

# Add a dropdown menu to the sidebar for the user to select a model
model = st.sidebar.selectbox("OpenAI Model", ["gpt-3.5-turbo", "gpt-4", "text-davinci-003", "code-davinci-002", "code-davinci-003"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if primer_desc is None or primer_code is None:
        st.error("Please upload your financial data before asking questions.")
        st.stop()

    formatted_question = format_question(primer_desc, primer_code, prompt, model_type=model)

    visualization_code = run_request(formatted_question, model, openai_api_key)

    if "visualize" in prompt and "data" in prompt:
        st.write("Here's a visualization of your data...")
        try:
            exec(visualization_code)
        except Exception as e:
            warnings.warn(f"An error occurred: {e}")
        st.session_state["messages"].append({"role": "assistant", "content": "I've visualized your financial data above."})
    else:
        openai.api_key = openai_api_key
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = openai.ChatCompletion.create(
            model=model, messages=st.session_state.messages
        )
        msg = response.choices[0].message
        st.session_state.messages.append(msg)
        st.chat_message("assistant").write(msg.content)