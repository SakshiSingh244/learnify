import sqlite3

# 📌 Connect to database (or create if it doesn't exist)
conn = sqlite3.connect("study_progress.db")
cursor = conn.cursor()

# ✅ Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    name TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);
""")
conn.commit()

# 📌 Add a subject
def add_subject(name):
    cursor.execute("INSERT OR IGNORE INTO subjects (name) VALUES (?)", (name,))
    conn.commit()

# 📌 Add topics to a subject
def add_topic(subject_name, topic_name):
    cursor.execute("SELECT id FROM subjects WHERE name = ?", (subject_name,))
    subject = cursor.fetchone()
    
    if subject:
        subject_id = subject[0]
        cursor.execute("INSERT INTO topics (subject_id, name) VALUES (?, ?)", (subject_id, topic_name))
        conn.commit()
    else:
        print("⚠️ Subject not found!")

# 📌 Mark topic as completed
def mark_topic_completed(topic_name):
    cursor.execute("UPDATE topics SET completed = 1 WHERE name = ?", (topic_name,))
    conn.commit()

# 📌 Fetch progress for a subject
def get_progress(subject_name):
    cursor.execute("""
        SELECT t.name, t.completed 
        FROM topics t 
        JOIN subjects s ON t.subject_id = s.id 
        WHERE s.name = ?
    """, (subject_name,))
    
    topics = cursor.fetchall()
    
    completed = sum(1 for t in topics if t[1] == 1)
    total = len(topics)
    progress = (completed / total * 100) if total > 0 else 0

    return topics, progress

# ✅ Sample Data
add_subject("Mathematics")
add_topic("Mathematics", "Algebra")
add_topic("Mathematics", "Calculus")

# ✅ Test marking progress
mark_topic_completed("Algebra")
topics, progress = get_progress("Mathematics")

print("Progress:", progress, "%")
print("Topics:", topics)

# Close connection
conn.close()
