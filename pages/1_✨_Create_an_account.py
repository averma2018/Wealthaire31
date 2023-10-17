import streamlit as st
import hashlib
import sqlite3
import re
from config import apply_custom_styles
apply_custom_styles()

conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable(c):
    c.execute('CREATE TABLE IF NOT EXISTS usertable(email TEXT PRIMARY KEY, password TEXT)')

def add_userdata(c, email, password):
    c.execute('INSERT INTO usertable(email, password) VALUES (?, ?)', (email, password))
    c.connection.commit()

def email_exists(c, email):
    c.execute('SELECT * FROM usertable WHERE email = ?', (email,))
    data = c.fetchall()
    return len(data) > 0

def valid_email(email):
    # Basic regex for email validation
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

def display(c):
    st.subheader("Create an account")
    email = st.text_input("email")
    password = st.text_input("password", type='password')

    if st.button("Signup"):
        create_usertable(c)
        if not valid_email(email):
            st.warning("Please enter a valid email address.")
            return

        if email_exists(c, email):
            st.warning("A user with this email address already exists.")
            return

        hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
        add_userdata(c, email, hashed_pw)
        st.session_state.logged_in = True
        st.success("Signed up successfully!")

# Call the display function directly.
display(c)

if 'logged_in' in st.session_state and st.session_state.logged_in:
    pass 

    # Checking for the existence of 'email' in session_state before accessing
    email = st.session_state.get('email', 'Unknown Email')
    
    # Add the account section in the sidebar
    st.sidebar.write("Account")
    st.sidebar.write(f"Signed in with {email}")  # Fetching email dynamically from session state
    if st.sidebar.button("Sign out"):
        st.session_state.logged_in = False
        st.write("Logged out successfully. See you next time!")
