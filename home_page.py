import streamlit as st
import app  # ✅ Import app.py to generate chapters & topics
import sqlite3

def save_roadmap(user_id, subject, topics):
    """Save roadmap to database."""
    conn = sqlite3.connect("roadmap.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO roadmaps (user_id, subject, progress) VALUES (?, ?, ?)",
        (user_id, subject, 0),  # Start with 0% progress
    )
    conn.commit()
    conn.close()

def home_page():
    st.title("🏠 Study Roadmap - Home")

    # ✅ Ensure user is logged in
    if "user_id" not in st.session_state:
        st.warning("Please log in first.")
        st.stop()

    user_id = st.session_state["user_id"]

    st.subheader(f"Welcome back, User {user_id}!")

    # Input for new roadmap
    st.write("### Create a New Study Roadmap")
    subject = st.text_input("Enter Subject Name")
    days = st.number_input("Enter Number of Days", min_value=1, step=1)

    if st.button("Generate Roadmap"):
        if subject:
            # ✅ Generate roadmap using app.py
            roadmap = app.get_chapters_and_topics(subject)

            if roadmap:
                # ✅ Save roadmap & navigate to roadmap page
                save_roadmap(user_id, subject, roadmap)
                st.session_state["roadmap"] = roadmap
                st.session_state["subject"] = subject
                st.session_state["current_page"] = "roadmap"
                st.rerun()
            else:
                st.error("Failed to generate roadmap. Try again.")
        else:
            st.warning("Please enter a subject name.")

    # Logout button
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
