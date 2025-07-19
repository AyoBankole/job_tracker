from data_base import get_db_connection
from datetime import date, timedelta

# ----- User Functions -----
def register_user(fellow_id, full_name, email):
    """Register a new user with Fellow ID; if ID exists, return existing user."""
    conn = get_db_connection()
    if not conn: return None
    user_id = None
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE fellow_id = %s", (fellow_id,))
            row = cur.fetchone()
            if row:
                user_id = row[0]
            else:
                cur.execute("""
                    INSERT INTO users (fellow_id, full_name, email)
                    VALUES (%s, %s, %s) RETURNING id
                """, (fellow_id, full_name, email))
                user_id = cur.fetchone()[0]
                conn.commit()
    finally:
        conn.close()
    return user_id

def get_user_by_fellow_id(fellow_id):
    """Retrieve user info by Fellow ID."""
    conn = get_db_connection()
    if not conn: return None
    user = None
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE fellow_id = %s", (fellow_id,))
            user = cur.fetchone()
    finally:
        conn.close()
    return user

# ----- Job Application Functions -----
def add_application(user_id, company, job_title, application_date):
    conn = get_db_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO applications (user_id, company, job_title, application_date)
                VALUES (%s, %s, %s, %s)
            """, (user_id, company, job_title, application_date))
            conn.commit()
    finally:
        conn.close()

def get_applications(user_id):
    conn = get_db_connection()
    if not conn: return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM applications WHERE user_id = %s ORDER BY application_date DESC", (user_id,))
            rows = cur.fetchall()
            return rows
    finally:
        conn.close()

# ----- Scholarship Functions -----
def add_scholarship(user_id, scholarship_name, application_date, deadline):
    conn = get_db_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO scholarships (user_id, scholarship_name, application_date, deadline)
                VALUES (%s, %s, %s, %s)
            """, (user_id, scholarship_name, application_date, deadline))
            conn.commit()
    finally:
        conn.close()

def get_scholarships(user_id):
    conn = get_db_connection()
    if not conn: return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM scholarships WHERE user_id = %s ORDER BY deadline ASC", (user_id,))
            rows = cur.fetchall()
            return rows
    finally:
        conn.close()

# --- Function for In-App Notifications ---
def get_upcoming_scholarship_deadlines(user_id, days_ahead=7):
    """Fetch scholarships with deadlines in the next X days for a user."""
    conn = get_db_connection()
    if not conn: return []
    try:
        with conn.cursor() as cur:
            today = date.today()
            future_date = today + timedelta(days=days_ahead)
            cur.execute("""
                SELECT scholarship_name, deadline
                FROM scholarships
                WHERE user_id = %s AND deadline BETWEEN %s AND %s
                ORDER BY deadline ASC
            """, (user_id, today, future_date))
            upcoming_scholarships = cur.fetchall()
            return upcoming_scholarships
    finally:
        conn.close()
