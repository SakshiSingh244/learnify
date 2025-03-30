import streamlit as st
import sqlite3
from database import add_user, init_db

def login_page():
    st.title("📚 Study Roadmap - Login")

    # Initialize Database
    init_db()

    # Sidebar Menu
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Select Option", menu, key="login_selectbox")

    if choice == "Login":
        st.subheader("Login to Your Account")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            conn = sqlite3.connect("roadmap.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                st.session_state["user_id"] = user[0]  # Save user ID
                st.session_state["logged_in"] = True
                st.session_state["page"] = "frontend"  # ✅ Store page for navigation
                st.success("Logged in successfully! Redirecting...")
                st.rerun()  # Refresh the app to apply changes

    elif choice == "Sign Up":
        st.subheader("Create an Account")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Sign Up"):
            try:
                add_user(username, email, password)
                st.success("Account created successfully! Please log in.")
            except sqlite3.IntegrityError:
                st.error("Username or email already exists.")

# ✅ Check session state and navigate accordingly
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    if "page" in st.session_state and st.session_state["page"] == "frontend":
        import frontend
        frontend.main()  # ✅ Call frontend.py function
    else:
        login_page()
else:
    login_page()
