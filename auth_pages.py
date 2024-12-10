import streamlit as st
import re
import requests

# API endpoint URL (make sure to replace with your actual endpoint URL)
API_BASE_URL = 'http://localhost:5000'


def show_sign_up_page():
    st.title("Sign Up")

    # User input for Sign Up
    username = st.text_input("Enter Email", key="sign_up_username")
    password = st.text_input("Enter Password", type="password", key="sign_up_password")

    # Unique key for the button
    if st.button("Sign Up", key="sign_up_button"):
        if username and password:
            if validate_email(username) and validate_password(password):
                # API call for sign-up
                response = requests.post(f'{API_BASE_URL}/sign_up', json={"username": username, "password": password})
                data = response.json()

                if response.status_code == 200:
                    st.success(data.get("message", "Sign up successful!"))
                else:
                    st.error(data.get("error", "Sign up failed."))
            else:
                st.error("Invalid email or password format.")
        else:
            st.error("Please fill in both fields.")


def show_login_page():
    st.title("Login")

    # User input for Login
    username = st.text_input("Enter Email", key="login_username")
    password = st.text_input("Enter Password", type="password", key="login_password")

    # Unique key for the button
    if st.button("Login", key="login_button"):
        if username and password:
            if validate_email(username) and validate_password(password):
                # API call for login
                response = requests.post(f'{API_BASE_URL}/login', json={"username": username, "password": password})
                data = response.json()

                if response.status_code == 200:
                    st.success(data.get("message", "Login successful!"))
                    # Here you might want to redirect or change the state for a logged-in user
                else:
                    st.error(data.get("message", "Login failed."))
            else:
                st.error("Invalid email or password format.")
        else:
            st.error("Please fill in both fields.")


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


def validate_password(password):
    has_letter = re.search(r'[a-zA-Z]', password)
    has_number = re.search(r'[0-9]', password)
    return has_letter and has_number


def main():
    st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page", ["Home", "Sign up", "Login"])

    if page == "Home":
        st.title("Home Page")

    elif page == "Sign Up":
        show_sign_up_page()

    elif page == "Login":
        show_login_page()


if __name__ == "__main__":
    main()
