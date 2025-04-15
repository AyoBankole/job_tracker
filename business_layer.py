# business_logic.py
import sqlite3
from data_base import DB_FILE, create_connection

# ----- User Functions -----
def register_user(full_name, education_level, university, course, email):
    """Register a new user with details; if email exists, return existing user ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Check if user already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    if row:
        conn.close()
        return row[0]  # Return existing user id

    # Insert new user with full details
    cursor.execute("""
        INSERT INTO users (full_name, education_level, university, course, email)
        VALUES (?, ?, ?, ?, ?)
    """, (full_name, education_level, university, course, email))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def update_user(user_id, full_name, education_level, university, course, email):
    """Update an existing user's details."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET full_name = ?, education_level = ?, university = ?, course = ?, email = ?
        WHERE id = ?
    """, (full_name, education_level, university, course, email, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    """Delete a user by user_id."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    """Retrieve user info by email."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

# ----- Job Application Functions -----
def add_application(user_id, company, job_title, application_date, status="Pending"):
    """Insert a new job application record for a user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO applications (user_id, company, job_title, application_date, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, company, job_title, application_date, status))
    conn.commit()
    conn.close()

def update_application(application_id, company, job_title, application_date, status):
    """Update an existing job application entry."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE applications
        SET company = ?, job_title = ?, application_date = ?, status = ?
        WHERE id = ?
    """, (company, job_title, application_date, status, application_id))
    conn.commit()
    conn.close()

def delete_application(application_id):
    """Delete a job application entry."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE id = ?", (application_id,))
    conn.commit()
    conn.close()

def get_applications(user_id):
    """Fetch all job applications for a given user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# ----- Scholarship Functions -----
def add_scholarship(user_id, scholarship_name, application_date, deadline, status="Pending"):
    """Insert a new scholarship application record for a user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scholarships (user_id, scholarship_name, application_date, deadline, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, scholarship_name, application_date, deadline, status))
    conn.commit()
    conn.close()

def update_scholarship(scholarship_id, scholarship_name, application_date, deadline, status):
    """Update an existing scholarship entry."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE scholarships
        SET scholarship_name = ?, application_date = ?, deadline = ?, status = ?
        WHERE id = ?
    """, (scholarship_name, application_date, deadline, status, scholarship_id))
    conn.commit()
    conn.close()

def delete_scholarship(scholarship_id):
    """Delete a scholarship entry."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scholarships WHERE id = ?", (scholarship_id,))
    conn.commit()
    conn.close()

def get_scholarships(user_id):
    """Fetch all scholarship applications for a given user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scholarships WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# ----- Reminder Management Functions -----
def add_reminder(application_id, reminder_date, message):
    """Add a reminder for a job application or scholarship (linked through application_id)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reminders (application_id, reminder_date, message)
        VALUES (?, ?, ?)
    """, (application_id, reminder_date, message))
    conn.commit()
    reminder_id = cursor.lastrowid
    conn.close()
    return reminder_id

def update_reminder(reminder_id, reminder_date, message):
    """Update an existing reminder."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE reminders
        SET reminder_date = ?, message = ?
        WHERE id = ?
    """, (reminder_date, message, reminder_id))
    conn.commit()
    conn.close()

def delete_reminder(reminder_id):
    """Delete a reminder."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    conn.commit()
    conn.close()

def get_reminders_for_user(user_id):
    """
    Fetch all reminders for a user by joining the reminders with the applications table.
    This assumes that reminders are linked to applications.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.id, r.application_id, r.reminder_date, r.message
        FROM reminders r
        JOIN applications a ON r.application_id = a.id
        WHERE a.user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

