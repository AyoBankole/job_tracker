import streamlit as st
import datetime
import pandas as pd
from business_layer import (
    add_application, get_applications,
    add_scholarship, get_scholarships,
    get_upcoming_scholarship_deadlines
)

# --- Page Configuration ---
st.set_page_config(
    page_title="Application Tracker",
    page_icon="📝",
    layout="wide"
)

# --- NEW "Midnight Blue" CSS Theme ---
st.markdown("""
<style>
/* --- Google Font Import --- */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap');

/* --- Root Variables for "Midnight Blue" Theme --- */
:root {
    --primary-color: #0a2540;    /* Midnight Blue */
    --accent-color: #d4af37;     /* Gold for accents */
    --background-color: #f0f2f6; /* Light Gray */
    --card-background-color: #ffffff;
    --text-color: #334155;       /* Slate */
    --subtle-text-color: #64748b;
    --border-color: #e2e8f0;
}

/* --- Global Styles --- */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    color: var(--text-color);
}
.stApp {
    background-color: var(--background-color);
}

/* --- Typography --- */
h1, h2, h3 {
    color: var(--primary-color);
    font-weight: 500;
}

/* --- Main Containers & Cards --- */
[data-testid="stExpander"], [data-testid="stForm"] {
    background-color: var(--card-background-color);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 8px 24px rgba(149, 157, 165, 0.1);
    margin-bottom: 1rem;
}
[data-testid="stExpander"] > div:first-child {
    font-weight: 500;
}

/* --- Button Styling --- */
div.stButton > button {
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 12px 24px;
    margin-top: 1rem;
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.3s ease-in-out;
}
div.stButton > button:hover {
    background-color: #1e3a5f;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
}

/* --- Input & Form Styling --- */
div.stTextInput > label, div.stDateInput > label {
    font-weight: 500;
    color: var(--subtle-text-color);
}
div.stTextInput > div > div > input, .stDateInput > div > div > input {
    border-radius: 8px;
    border: 1px solid var(--border-color);
    padding: 12px;
}
div.stTextInput > div > div > input:focus, .stDateInput > div > div > input:focus {
    border-color: var(--accent-color);
    box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2);
}

/* --- Dataframe/Table Styling --- */
.stDataFrame {
    border: none;
    border-radius: 12px;
    overflow: hidden;
}
.stDataFrame thead th {
    background-color: #f8fafc;
    color: var(--primary-color);
    font-weight: 500;
    font-size: 0.9rem;
    text-transform: uppercase;
    border-bottom: 2px solid var(--border-color);
}
.stDataFrame tbody tr:hover {
    background-color: #f1f5f9;
}

/* --- Notification/Alert Styling --- */
[data-testid="stAlert"] {
    border-radius: 8px;
    border-width: 1px;
    border-style: solid;
    padding: 1rem;
}
[data-testid="stAlert"][data-baseweb="notification"][kind="warning"] {
    background-color: #fffbeb;
    border-color: #facc15;
    color: #b45309;
}
[data-testid="stAlert"][data-baseweb="notification"][kind="info"] {
    background-color: #eff6ff;
    border-color: #60a5fa;
    color: #2563eb;
}

</style>
""", unsafe_allow_html=True)


# --- FIXED: More Robust Authentication Check ---
# This checks for all required keys to prevent the KeyError.
required_keys = ['logged_in', 'user_id', 'fellow_id', 'full_name']
if not all(st.session_state.get(key) for key in required_keys):
    st.error("You must be logged in to view this page.")
    st.info("Please go to the main page to log in.")
    st.stop()

# --- Helper function for CSV download ---
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# --- Page Content ---
st.title(f"Welcome, {st.session_state['full_name']}!")
st.markdown(f"Tracking applications for Fellow ID: **{st.session_state['fellow_id']}**")


user_id = st.session_state['user_id']

# --- In-App Notifications for Upcoming Deadlines ---
upcoming_deadlines = get_upcoming_scholarship_deadlines(user_id)
if upcoming_deadlines:
    st.subheader("🔔 Upcoming Deadlines!")
    for scholarship_name, deadline in upcoming_deadlines:
        days_left = (deadline - datetime.date.today()).days
        st.toast(f'Deadline for "{scholarship_name}" is in {days_left} days!', icon='⏰')
        if days_left <= 3:
            st.warning(f'**Urgent:** The deadline for **{scholarship_name}** is on **{deadline.strftime("%B %d, %Y")}** ({days_left} days left).', icon="🔥")
        else:
            st.info(f'Heads up: The deadline for **{scholarship_name}** is on **{deadline.strftime("%B %d, %Y")}** ({days_left} days left).', icon="💡")

# --- Main Layout with Columns ---
col1, col2 = st.columns(2)

with col1:
    # --- Job Application Section ---
    st.header("💼 Job Applications")
    with st.expander("Add a New Job Application"):
        with st.form("job_application_form", clear_on_submit=True):
            company = st.text_input("Company Name")
            job_title = st.text_input("Job Title")
            application_date = st.date_input("Application Date", datetime.date.today())
            job_submitted = st.form_submit_button("Add Job Application")
            if job_submitted and company and job_title:
                add_application(user_id, company, job_title, application_date)
                st.success("Job application added!")

    st.subheader("Your Job Applications")
    applications = get_applications(user_id)
    if applications:
        df_jobs = pd.DataFrame(applications, columns=['ID', 'User ID', 'Company', 'Job Title', 'Date', 'Status'])
        st.dataframe(df_jobs[['ID', 'Company', 'Job Title', 'Date', 'Status']], use_container_width=True)
        csv_jobs = convert_df_to_csv(df_jobs)
        st.download_button(
            label="Download Jobs as CSV",
            data=csv_jobs,
            file_name='job_applications.csv',
            mime='text/csv',
        )
    else:
        st.info("No job applications found. Add one above!")

with col2:
    # --- Scholarship Application Section ---
    st.header("🎓 Scholarship Applications")
    with st.expander("Add a New Scholarship Application"):
        with st.form("scholarship_form", clear_on_submit=True):
            scholarship_name = st.text_input("Scholarship Name")
            scholarship_application_date = st.date_input("Application Date", datetime.date.today())
            deadline = st.date_input("Deadline", datetime.date.today() + datetime.timedelta(days=30))
            sch_submitted = st.form_submit_button("Add Scholarship Application")
            if sch_submitted and scholarship_name:
                add_scholarship(user_id, scholarship_name, scholarship_application_date, deadline)
                st.success("Scholarship application added!")

    st.subheader("Your Scholarship Applications")
    scholarships = get_scholarships(user_id)
    if scholarships:
        df_sch = pd.DataFrame(scholarships, columns=['ID', 'User ID', 'Scholarship', 'Application Date', 'Deadline', 'Status'])
        st.dataframe(df_sch[['ID', 'Scholarship', 'Application Date', 'Deadline', 'Status']], use_container_width=True)
        csv_scholarships = convert_df_to_csv(df_sch)
        st.download_button(
            label="Download Scholarships as CSV",
            data=csv_scholarships,
            file_name='scholarship_applications.csv',
            mime='text/csv',
        )
    else:
        st.info("No scholarship applications found. Add one above!")