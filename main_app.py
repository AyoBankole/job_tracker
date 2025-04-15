import streamlit as st
import datetime
from business_layer import (
    register_user, update_user, delete_user, get_user_by_email,
    add_application, update_application, delete_application, get_applications,
    add_scholarship, update_scholarship, delete_scholarship, get_scholarships,
    add_reminder, update_reminder, delete_reminder, get_reminders_for_user
)
from data_base import create_connection, create_tables

# -- CUSTOM CSS STYLES WITH SDG8 THEME --
custom_css = """
<style>
/* Import Google Font: Roboto */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
html, body, [class*="css"] {
    font-family: 'Roboto', sans-serif;
}
/* SDG8 Theme Color Variables */
:root {
    --sdg-primary: #A21942;
    --sdg-secondary: #FD7F00;
    --sdg-background: #F7F7F7;
}
/* Apply background color */
.stApp {
    background-color: var(--sdg-background);
}
/* Header styling */
h1 { color: var(--sdg-primary); font-size: 3rem; text-align: center; }
h2, h3, h4 { color: var(--sdg-secondary); }
/* Button styling */
div.stButton > button {
    background-color: var(--sdg-primary);
    color: white;
    border: none;
    padding: 0.5em 1em;
    margin: 1em 0;
    border-radius: 5px;
    font-size: 1rem;
}
/* Input label styling */
div.stTextInput > label { color: var(--sdg-secondary); font-size: 1rem; }
/* Adding margins for content */
.css-1d391kg { padding: 2rem; }
/* Logo container styling for side-by-side images */
.logo-container { display: flex; justify-content: center; gap: 2rem; padding: 1rem; }
.logo-container img { max-width: 150px; height: auto; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Sidebar: User Registration with User Logo ---
import streamlit as st

# Initialize session state to store user info
if "registered" not in st.session_state:
    st.session_state.registered = False
if "full_name" not in st.session_state:
    st.session_state.full_name = ""

# Display image with user's name if registered, else default caption
caption = st.session_state.full_name if st.session_state.registered else "Welcome!"
st.sidebar.image("profile.png", width=100, caption=caption)  

st.sidebar.header("User Registration")
st.sidebar.markdown("Register to start tracking opportunities.")

with st.sidebar.form("registration_form"):
    full_name = st.text_input("Full Name")
    education_level = st.selectbox("Education Level", ["Select", "Undergraduate", "Graduate", "Postgraduate", "Other"])
    university = st.text_input("University")
    course = st.text_input("Course of Study")
    email = st.text_input("Email")
    reg_submitted = st.form_submit_button("Register")
    
    if reg_submitted:
        if all([full_name, education_level != "Select", university, course, email]):
            user_id = register_user(full_name, education_level, university, course, email)
            st.session_state.full_name = full_name
            st.session_state.registered = True
            st.sidebar.success(f"Welcome {full_name}! Registered successfully. Your User ID is {user_id}")
        else:
            st.sidebar.error("Please fill in all required fields.")

# --- Main Area: Display 3 Logos Side-by-Side ---
cols = st.columns(3)
with cols[0]:
    st.image("cropped-logo2.jpg", caption="MushinToTheWorld Foundation", width=150)
with cols[1]:
    st.image("grad.png", width=150)
with cols[2]:
    st.image("Mushin-Local-Government-1.jpg", caption="Mushin Local Government", width=150)

# Dedicated SDG Message
st.markdown("<h4 style='text-align: center; color: var(--sdg-secondary);'>Advancing Decent Work & Education Through Smart Tracking.</h4>", unsafe_allow_html=True)

# --- Initialize the Database ---
conn = create_connection()
if conn:
    create_tables(conn)
    conn.close()

st.title("Job & Scholarship Application Tracker")

# --- Dashboard: User Login ---
st.header("Dashboard")
st.markdown("Enter your registered email to continue and manage your applications.")
user_email = st.text_input("Registered Email", key="login_email")

if user_email:
    user = get_user_by_email(user_email)
    if user:
        user_id = user[0]
        st.write(f"Welcome, **{user[1]}** (User ID: {user_id})!")
        
        # --- Job Application Section ---
        st.subheader("Job Applications")
        st.markdown("Add your job applications below:")
        with st.form("job_application_form"):
            company = st.text_input("Company Name", key="company")
            job_title = st.text_input("Job Title", key="job_title")
            application_date = st.date_input("Application Date", datetime.date.today(), key="app_date")
            job_submitted = st.form_submit_button("Add Job Application")
            if job_submitted:
                add_application(user_id, company, job_title, application_date.isoformat())
                st.success("Job application added successfully!")
        
        st.subheader("Your Job Applications")
        applications = get_applications(user_id)
        if applications:
            for app in applications:
                st.markdown(f"**ID:** {app[0]}  |  **Company:** {app[2]}  |  **Job Title:** {app[3]}  |  **Date:** {app[4]}  |  **Status:** {app[5]}")
        else:
            st.info("No job applications found.")
        
        # --- Scholarship Application Section ---
        st.subheader("Scholarship Applications")
        st.markdown("Add your scholarship applications below:")
        with st.form("scholarship_form"):
            scholarship_name = st.text_input("Scholarship Name", key="scholarship_name")
            scholarship_application_date = st.date_input("Application Date", datetime.date.today(), key="scholarship_app_date")
            deadline = st.date_input("Deadline", datetime.date.today(), key="deadline")
            sch_submitted = st.form_submit_button("Add Scholarship Application")
            if sch_submitted:
                add_scholarship(user_id, scholarship_name, scholarship_application_date.isoformat(), deadline.isoformat())
                st.success("Scholarship application added successfully!")
        
        st.subheader("Your Scholarship Applications")
        scholarships = get_scholarships(user_id)
        if scholarships:
            for sch in scholarships:
                st.markdown(f"**ID:** {sch[0]}  |  **Scholarship:** {sch[2]}  |  **Date:** {sch[3]}  |  **Deadline:** {sch[4]}  |  **Status:** {sch[5]}")
        else:
            st.info("No scholarship applications found.")

        # --- Reminders Section ---
        st.subheader("Reminders")
        st.markdown("Set up reminders for your upcoming interviews or scholarship deadlines.")
        with st.form("reminder_form"):
            # For simplicity we ask for an Application ID from the user's applications.
            reminder_application_id = st.number_input("Application ID", min_value=1, step=1, key="rem_app_id")
            reminder_date = st.date_input("Reminder Date", datetime.date.today(), key="rem_date")
            reminder_message = st.text_input("Reminder Message", key="rem_message")
            rem_submitted = st.form_submit_button("Add Reminder")
            if rem_submitted:
                add_reminder(reminder_application_id, reminder_date.isoformat(), reminder_message)
                st.success("Reminder added successfully!")
        
        st.subheader("Your Reminders")
        reminders = get_reminders_for_user(user_id)
        if reminders:
            for rem in reminders:
                st.markdown(f"**Reminder ID:** {rem[0]}  |  **Application ID:** {rem[1]}  |  **Date:** {rem[2]}  |  **Message:** {rem[3]}")
        else:
            st.info("No reminders found.")

    else:
        st.error("Email not registered. Please register using the sidebar.")