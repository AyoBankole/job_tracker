import psycopg2
import streamlit as st
from config import DATABASE_URL

def get_db_connection():
    """Create a database connection to the PostgreSQL database."""
    if not DATABASE_URL:
        st.error("DATABASE_URL is not set. Please configure it in your environment.")
        return None
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except psycopg2.OperationalError as e:
        st.error(f"Could not connect to the database. Please check your configuration. Error: {e}")
    return conn

def create_tables():
    """Create or update tables for users, applications, and scholarships."""
    conn = get_db_connection()
    if conn is None:
        return
        
    try:
        with conn.cursor() as cur:
            # UPDATED: Users table now includes a hashed_password column
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    fellow_id TEXT UNIQUE NOT NULL,
                    full_name TEXT,
                    email TEXT,
                    hashed_password TEXT NOT NULL,      -- Added this line
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
            
            # Applications table (no changes from last version)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS applications (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    company TEXT NOT NULL,
                    job_title TEXT NOT NULL,
                    application_date DATE,
                    deadline DATE,
                    status TEXT DEFAULT 'Pending',
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)

            # Scholarships table (no changes from last version)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS scholarships (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    university_name TEXT NOT NULL,
                    scholarship_type TEXT NOT NULL,
                    course_of_study TEXT,
                    application_date DATE,
                    deadline DATE,
                    status TEXT DEFAULT 'Pending',
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
            conn.commit()
    except psycopg2.Error as e:
        st.error(f"Error creating tables: {e}")
    finally:
        if conn:
            conn.close()