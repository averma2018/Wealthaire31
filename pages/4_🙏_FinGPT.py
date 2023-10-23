from matplotlib import figure
import pandas as pd
import openai
import streamlit as st
from classes1 import get_primer, format_question, run_request
import warnings

warnings.filterwarnings("ignore")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_icon="fingpt_icon.png", layout="wide", page_title="FinGPT Data Analysis")

# Headers
st.title("FinGPT Data Analysis")
st.subheader("Analyze your data using OpenAI powered chatbot.")

# Sidebar information
st.sidebar.markdown("### Instructions")
st.sidebar.markdown("1. Upload your data file (CSV format).")
st.sidebar.markdown("2. Enter your OpenAI API key.")
st.sidebar.markdown("3. Ask a data analysis related question about the uploaded dataset.")

# API Key Input
openai_key = st.sidebar.text_input(label="OpenAI API Key:", help="Required for FinGPT data analysis.", type="password")

# List of OpenAI models
models = ["gpt-4", "gpt-3.5-turbo", "text-davinci-003", "gpt-3.5-turbo-instruct"]
selected_model = st.sidebar.selectbox("Choose an OpenAI Model:", models)


# Dataset upload
uploaded_file = st.sidebar.file_uploader("Upload your CSV data:", type="csv")

if uploaded_file:
    try:
        data = pd.read_csv(uploaded_file)
        st.write("Uploaded Data Preview:")
        st.dataframe(data.head())
        
        # User query input
        question = st.text_input("What data analysis would you like to perform?")
        analyze_btn = st.button("Analyze")
        
        if not openai_key.startswith('sk-'):
                st.error("Please enter a valid OpenAI API key.")
        elif analyze_btn and question:
          
                # Formulate the prompt and query OpenAI
                primer1, primer2 = get_primer(data,'df') 
                question_to_ask = format_question(primer1, primer2, question, selected_model)
                print(f"Using API key: {openai_key}")
               

                try:
                    df = data.copy()
                    answer = run_request(question_to_ask, openai_key, selected_model)
                    answer = primer2 + "\n" + answer
                    print("Generated Code:")
                    print(answer)

                    plot_area = st.empty()
                    exec(answer)
                    if 'fig' in locals():  # Check if a matplotlib figure 'fig' was created in the executed code
                        plot_area.pyplot(fig)
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.write("Please ensure your question matches the structure and columns of the uploaded data.")
    except pd.errors.ParserError:
        st.error("Error: Could not parse the uploaded CSV. Please ensure it's a valid CSV format.")    
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")

else:
    st.sidebar.warning("Please upload a CSV file to start analyzing.")

# Footer details
st.caption("Wealthaire, 2023")