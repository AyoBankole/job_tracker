from data_base import get_db_connection
from datetime import date, timedelta
import bcrypt # Import bcrypt

# --- User Functions (UPDATED) ---
def register_user(fellow_id, full_name, email, password):
    """Register a new user with a hashed password."""
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    conn = get_db_connection()
    if not conn: return None
    try:
        with conn.cursor() as cur:
            # Check if user already exists
            cur.execute("SELECT id FROM users WHERE fellow_id = %s", (fellow_id,))
            if cur.fetchone():
                return None # User already exists

            # Insert new user with hashed password
            cur.execute("""
                INSERT INTO users (fellow_id, full_name, email, hashed_password)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (fellow_id, full_name, email, hashed_password))
            user_id = cur.fetchone()[0]
            conn.commit()
            return user_id
    finally:
        conn.close()

def verify_user(fellow_id, password):
    """Verify user login by checking the hashed password."""
    conn = get_db_connection()
    if not conn: return None
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, fellow_id, full_name, hashed_password FROM users WHERE fellow_id = %s", (fellow_id,))
            user_record = cur.fetchone()
            if user_record:
                # Check if the provided password matches the stored hash
                hashed_password_from_db = user_record[3]
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password_from_db.encode('utf-8')):
                    # Return user data (without the hash) if password is correct
                    return user_record[:3] # Returns (id, fellow_id, full_name)
    finally:
        conn.close()
    return None

# --- Other functions (no changes) ---
def add_application(user_id, company, job_title, application_date, deadline):
    # This function remains the same
    conn = get_db_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO applications (user_id, company, job_title, application_date, deadline)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, company, job_title, application_date, deadline))
            conn.commit()
    finally:
        conn.close()

def get_applications(user_id):
    # This function remains the same
    conn = get_db_connection()
    if not conn: return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM applications WHERE user_id = %s ORDER BY application_date DESC", (user_id,))
            rows = cur.fetchall()
            return rows
    finally:
        conn.close()

def update_job_status(application_id, new_status):
    # This function remains the same
    conn = get_db_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE applications SET status = %s WHERE id = %s", (new_status, application_id))
            conn.commit()
    finally:
        conn.close()
        
def add_scholarship(user_id, university_name, scholarship_type, course_of_study, application_date, deadline):
    # This function remains the same
    conn = get_db_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO scholarships (user_id, university_name, scholarship_type, course_of_study, application_date, deadline)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, university_name, scholarship_type, course_of_study, application_date, deadline))
            conn.commit()
    finally:
        conn.close()

def get_scholarships(user_id):
    # This function remains the same
    conn = get_db_connection()
    if not conn: return []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM scholarships WHERE user_id = %s ORDER BY deadline ASC", (user_id,))
            rows = cur.fetchall()
            return rows
    finally:
        conn.close()
        
def get_upcoming_scholarship_deadlines(user_id, days_ahead=7):
    # This function remains the same
    conn = get_db_connection()
    if not conn: return []
    try:
        with conn.cursor() as cur:
            today = date.today()
            future_date = today + timedelta(days=days_ahead)
            cur.execute("""
                SELECT university_name, course_of_study, deadline
                FROM scholarships
                WHERE user_id = %s AND deadline BETWEEN %s AND %s
                ORDER BY deadline ASC
            """, (user_id, today, future_date))
            upcoming_scholarships = cur.fetchall()
            return upcoming_scholarships
    finally:
        conn.close()