import streamlit as st
import json
import sqlite3
from app import get_chapters_and_topics
from url import get_top_articles
from yt import get_top_youtube_video
from qna_generator import generate_qna
from database import save_roadmap, get_user_roadmaps

def display_roadmap():
    if "roadmap" not in st.session_state:
        return

    st.subheader("📝 Your Study Plan")
    for chapter, topics in st.session_state["roadmap"].items():
        st.subheader(f"📖 {chapter}")
        for topic in topics:
            st.write(f"- **{topic}**")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button(f"🔗 Articles: {topic}", key=f"art_{chapter}_{topic}"):
                    articles = get_top_articles(topic)
                    if articles:
                        for article in articles:
                            if isinstance(article, dict) and "title" in article and "url" in article:
                                st.markdown(f"[{article['title']}]({article['url']})")
                            else:
                                st.write(article)
                    else:
                        st.write("No articles found.")

            with col2:
                if st.button(f"▶ YouTube: {topic}", key=f"yt_{chapter}_{topic}"):
                    video_info = get_top_youtube_video(topic)
                    if "url" in video_info and video_info["url"]:
                        st.markdown(f"[🎥 {video_info['title']}]({video_info['url']})")
                    else:
                        st.write("No relevant video found.")

            with col3:
                if st.button(f"📝 Q&A: {topic}", key=f"qna_{chapter}_{topic}"):
                    qna = generate_qna(topic)
                    if isinstance(qna, dict):
                        for q, a in qna.items():
                            st.write(f"**Q:** {q}")
                            st.write(f"**A:** {a}")
                            st.write("---")
                    else:
                        st.write("Failed to generate Q&A.")


def main():
    st.title("📚 Study Roadmap Generator")

    # Check if user is logged in
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("⚠️ Please log in first.")
        st.session_state["page"] = "login"
        st.rerun()

    user_id = st.session_state.get("user_id")

    # ✅ Load Previous Roadmaps
    previous_roadmaps = get_user_roadmaps(user_id)
    roadmap_options = {f"{row['subject']} (ID: {row['id']})": row 
                      for row in previous_roadmaps if 'subject' in row and 'id' in row}
    selected_roadmap = st.selectbox("📜 Load Previous Roadmap:", ["None"] + list(roadmap_options.keys()))

    # If a previous roadmap is selected, load it
    if selected_roadmap != "None":
        selected_data = roadmap_options[selected_roadmap]
        roadmap_id = selected_data["id"]
        subject = selected_data["subject"]
        topics_data = selected_data.get("topics", "{}")
        
        try:
            # Handle both string JSON and already parsed dict
            if isinstance(topics_data, str):
                roadmap = json.loads(topics_data)
            else:
                roadmap = topics_data
            
            if not isinstance(roadmap, dict):
                st.error("❌ Invalid roadmap format in database")
            else:
                st.session_state["roadmap"] = roadmap
                st.success(f"✅ Loaded roadmap for **{subject}**")
                display_roadmap()  # Display immediately after loading
                
        except json.JSONDecodeError:
            st.error("❌ Failed to parse roadmap data from database")
        except Exception as e:
            st.error(f"❌ Error loading roadmap: {str(e)}")

    # User Input for New Roadmap
    st.subheader("📌 Generate a New Roadmap")
    subject = st.text_input("Enter Subject Name:")
    days = st.number_input("Number of Days to Complete:", min_value=1, step=1)

    if st.button("Generate Roadmap"):
        if subject:
            roadmap_str = get_chapters_and_topics(subject)
            try:
                roadmap = json.loads(roadmap_str) if isinstance(roadmap_str, str) else roadmap_str
                st.session_state["roadmap"] = roadmap

                # ✅ Save roadmap to database
                save_roadmap(user_id, subject, roadmap)
                st.success("📌 New roadmap saved successfully!")
                display_roadmap()  # Display immediately after generation

            except json.JSONDecodeError:
                st.error("❌ Failed to generate roadmap. Invalid format from API.")
        else:
            st.warning("⚠️ Please enter a subject name.")

    # Only show the roadmap if it hasn't already been shown above
    if selected_roadmap == "None" and "roadmap" in st.session_state:
        display_roadmap()

if __name__ == "__main__":
    main()