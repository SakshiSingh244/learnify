import sqlite3
import json

def init_db():
    
    conn = sqlite3.connect("roadmap.db")
    cursor = conn.cursor()
    
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        email TEXT UNIQUE,
                        password TEXT)''')

    
    cursor.execute('''CREATE TABLE IF NOT EXISTS roadmaps (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        subject TEXT,
                        topics TEXT DEFAULT '{}',  -- Default empty JSON object
                        progress TEXT DEFAULT '{}',  -- Default empty JSON object
                        FOREIGN KEY (user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

def add_user(username, email, password):
    
    conn = sqlite3.connect("roadmap.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                       (username, email, password))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Username or email already exists.")
    finally:
        conn.close()

def save_roadmap(user_id, subject, topics):
    """Save a roadmap for a user."""
    conn = sqlite3.connect("roadmap.db")
    cursor = conn.cursor()
    
    
    topics_json = json.dumps(topics) if topics else "{}"
    progress_json = json.dumps({})  

    cursor.execute("INSERT INTO roadmaps (user_id, subject, topics, progress) VALUES (?, ?, ?, ?)", 
                   (user_id, subject, topics_json, progress_json))
    conn.commit()
    conn.close()

def get_user_roadmaps(user_id):
    
    conn = sqlite3.connect("roadmap.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, subject, topics FROM roadmaps WHERE user_id = ?", (user_id,))
    roadmaps = cursor.fetchall()
    conn.close()
    
    
    roadmap_list = []
    for roadmap in roadmaps:
        roadmap_id, subject, topics_json = roadmap
        try:
            topics = json.loads(topics_json) if topics_json else {}
        except json.JSONDecodeError:
            topics = {} 

        roadmap_list.append({
            "id": roadmap_id,
            "subject": subject,
            "topics": topics
        })
    
    return roadmap_list

def get_roadmap_by_id(roadmap_id):
    
    conn = sqlite3.connect("roadmap.db")
    cursor = conn.cursor()
    cursor.execute("SELECT subject, topics FROM roadmaps WHERE id = ?", (roadmap_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        subject, topics_json = result
        try:
            topics = json.loads(topics_json) if topics_json else {}
        except json.JSONDecodeError:
            topics = {}
        return {"subject": subject, "topics": topics}
    
    return None
