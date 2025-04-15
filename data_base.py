# data_base.py
import sqlite3

DB_FILE = "job_tracker.db"

def create_connection(db_file=DB_FILE):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        print("Database connection established.")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_tables(conn):
    """Create tables for users, applications, scholarships, and reminders."""
    try:
        cursor = conn.cursor()
        # Users table with extra registration fields
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                education_level TEXT,
                university TEXT,
                course TEXT,
                email TEXT UNIQUE,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        # Applications table linked to users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                company TEXT NOT NULL,
                job_title TEXT NOT NULL,
                application_date TEXT,
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        # Scholarships table linked to users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scholarships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                scholarship_name TEXT NOT NULL,
                application_date TEXT,
                deadline TEXT,
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        # Reminders table linked to applications (or scholarships if needed)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER,
                reminder_date TEXT,
                message TEXT,
                FOREIGN KEY(application_id) REFERENCES applications(id)
            )
        """)
        conn.commit()
        print("Tables created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
        
# def drop_users_table(conn):
#     cursor = conn.cursor()
#     cursor.execute("DROP TABLE IF EXISTS users")
#     conn.commit()
#     print("Users table dropped.")

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        create_tables(conn)
        conn.close()