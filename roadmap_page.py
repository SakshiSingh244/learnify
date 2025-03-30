import streamlit as st
import sqlite3

def get_user_roadmap(user_id):
    """Retrieve roadmap data from database."""
    conn = sqlite3.connect("roadmap.db")
    cursor = conn.cursor()
    cursor.execute("SELECT subject, progress FROM roadmaps WHERE user_id=?", (user_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def roadmap_page():
    st.title("📚 Your Study Roadmap")

    if "user_id" not in st.session_state:
        st.error("Please log in first.")
        return

    user_id = st.session_state["user_id"]
    roadmap_data = get_user_roadmap(user_id)

    if not roadmap_data:
        st.warning("No roadmap found. Please create one.")
        return

    subject = st.session_state.get("subject", "Unknown Subject")
    topics = st.session_state.get("roadmap", {})

    # Display progress overview
    st.write(f"### Subject: {subject}")
    total_topics = sum(len(topics[chapter]) for chapter in topics)
    completed_topics = sum(st.session_state.get(f"{subject}_{topic}", 0) for chapter in topics for topic in topics[chapter])
    
    overall_progress = (completed_topics / total_topics) * 100 if total_topics else 0

    st.progress(overall_progress / 100)
    st.write(f"### Overall Progress: {overall_progress:.1f}%")

    # Display topics
    for chapter, chapter_topics in topics.items():
        with st.expander(f"📖 {chapter}"):
            for topic in chapter_topics:
                col1, col2 = st.columns([3, 1])
                col1.write(f"**{topic}**")
                progress_key = f"{subject}_{topic}"
                progress_val = st.session_state.get(progress_key, 0)
                col2.progress(progress_val / 10)

                st.button("📄 Articles", key=f"art_{subject}_{topic}")
                st.button("🎥 YouTube Video", key=f"yt_{subject}_{topic}")
                st.button("❓ Q&A", key=f"qa_{subject}_{topic}")
                st.divider()

    # ✅ Back to home button
    if st.button("🏠 Back to Home"):
        st.session_state["current_page"] = "home"
        st.rerun()
