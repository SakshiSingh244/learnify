import streamlit as st
from login_page import login_page
from home_page import home_page
from roadmap_page import roadmap_page

# ✅ Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "login"

# ✅ Page Router
if st.session_state["current_page"] == "login":
    login_page()
elif st.session_state["current_page"] == "home":
    home_page()
elif st.session_state["current_page"] == "roadmap":
    roadmap_page()
