import streamlit as st
import hashlib
import sqlite3
from streamlit_config import apply_custom_styles
apply_custom_styles()

def create_cursor():
    conn = sqlite3.connect('data.db')
    return conn, conn.cursor()

def login_user(c, email, password):
    c.execute('SELECT * FROM usertable WHERE email = ? AND password = ?', (email, password))
    data = c.fetchall()
    return data

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.subheader("Login")
    email = st.text_input("email")
    password = st.text_input("password", type='password')
    if st.button("Sign In"):
        conn, c = create_cursor()
        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
        result = login_user(c, email, hashed_pw)
        if result:
            st.session_state.logged_in = True
            st.session_state.email = email  # Store email in session state
            st.success("Logged In")
        else:
            st.error("Incorrect email or password")
        conn.close()

# Else part handles the logged-in state
else:
    st.subheader("Welcome back! 👋")

    # Checking for the existence of 'email' in session_state before accessing
    email = st.session_state.get('email', 'Unknown Email')
    
    # Add the account section in the sidebar
    st.sidebar.write("Account")
    st.sidebar.write(f"Signed in as {email}")  # Fetching email dynamically from session state
    
    if st.sidebar.button("Sign out"):
        st.session_state.logged_in = False
        st.session_state.logged_out = True  # Add a logged out flag to the session state
        st.subheader("Logged out successfully. See you next time!")

if 'logged_out' in st.session_state and st.session_state.logged_out:
    st.subheader("Logged out successfully. See you next time!")
