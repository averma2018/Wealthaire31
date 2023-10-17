import streamlit as st
import sqlite3
from config import apply_custom_styles
apply_custom_styles()


def create_cursor():
    conn = sqlite3.connect('data.db')
    return conn.cursor()

st.image("assets/wealthaire logo.svg")  # Adjust your logo image path


if 'logged_in' in st.session_state and st.session_state.logged_in:
    st.write("Welcome Back!")

    # Checking for the existence of 'email' in session_state before accessing
    email = st.session_state.get('email', 'Unknown Email')
    
    # Add the account section in the sidebar
    st.sidebar.write("Account")
    st.sidebar.write(f"Signed in with {email}")  # Fetching email dynamically from session state
    if st.sidebar.button("Sign out"):
        st.session_state.logged_in = False
        st.write("Logged out successfully. See you next time!")

