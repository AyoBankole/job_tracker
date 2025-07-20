import streamlit as st
import datetime
import pandas as pd
from business_layer import (
    add_application, get_applications, update_job_status,
    add_scholarship, get_scholarships,
    get_upcoming_scholarship_deadlines
)

# --- Page Configuration ---
st.set_page_config(
    page_title="Application Tracker",
    page_icon="📝",
    layout="wide"
)

# --- Authentication Check ---
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

# --- In-App Notifications for Upcoming Deadlines (UPDATED) ---
upcoming_deadlines = get_upcoming_scholarship_deadlines(user_id)
if upcoming_deadlines:
    st.subheader("🔔 Upcoming Scholarship Deadlines!")
    # UPDATED: Loop now unpacks three values: university, course, and deadline
    for university, course, deadline in upcoming_deadlines:
        days_left = (deadline - datetime.date.today()).days
        # UPDATED: Notification message is more descriptive
        notification_text = f'"{course}" at {university}'
        
        st.toast(f'Deadline for {notification_text} is in {days_left} days!', icon='⏰')
        if days_left <= 3:
            st.warning(f'**Urgent:** The deadline for **{notification_text}** is on **{deadline.strftime("%B %d, %Y")}** ({days_left} days left).', icon="🔥")
        else:
            st.info(f'Heads up: The deadline for **{notification_text}** is on **{deadline.strftime("%B %d, %Y")}** ({days_left} days left).', icon="💡")

# --- Main Layout with Columns ---
col1, col2 = st.columns(2)

with col1:
    # --- Job Application Section (no changes) ---
    st.header("💼 Job Applications")
    with st.expander("Add a New Job Application"):
        with st.form("job_application_form", clear_on_submit=True):
            company = st.text_input("Company Name")
            job_title = st.text_input("Job Title")
            application_date = st.date_input("Application Date", datetime.date.today())
            deadline = st.date_input("Application Deadline", datetime.date.today() + datetime.timedelta(days=30))
            
            job_submitted = st.form_submit_button("Add Job Application")
            if job_submitted and company and job_title:
                add_application(user_id, company, job_title, application_date, deadline)
                st.success("Job application added!")

    st.subheader("Your Job Applications")
    applications = get_applications(user_id)
    if applications:
        job_cols = ['ID', 'User ID', 'Company', 'Job Title', 'Applied', 'Deadline', 'Status', 'Created At']
        df_jobs_orig = pd.DataFrame(applications, columns=job_cols)

        edited_df = st.data_editor(
            df_jobs_orig[['ID', 'Company', 'Job Title', 'Status', 'Deadline', 'Created At']],
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Pending", "Submitted", "Interviewing", "Offer", "Rejected"],
                    required=True,
                )
            },
            hide_index=True,
            use_container_width=True,
            key="job_editor"
        )

        for index, row in edited_df.iterrows():
            original_row = df_jobs_orig.iloc[index]
            if row['Status'] != original_row['Status']:
                update_job_status(row['ID'], row['Status'])
                st.toast(f"Updated status for {row['Job Title']} to {row['Status']}")
        
        csv_jobs = convert_df_to_csv(df_jobs_orig)
        st.download_button(
            label="Download Jobs as CSV",
            data=csv_jobs,
            file_name='job_applications.csv',
            mime='text/csv',
        )
    else:
        st.info("No job applications found. Add one above!")

with col2:
    # --- Scholarship Application Section (no changes) ---
    st.header("🎓 Scholarship Applications")
    with st.expander("Add a New Scholarship Application"):
        with st.form("scholarship_form", clear_on_submit=True):
            university_name = st.text_input("University Name")
            scholarship_type = st.selectbox("Scholarship Type", ["Full Scholarship", "Partial Funding", "Stipend Only", "Tuition Waiver"])
            course_of_study = st.text_input("Course of Study")
            application_date = st.date_input("Application Date", datetime.date.today())
            deadline = st.date_input("Application Deadline", datetime.date.today() + datetime.timedelta(days=60))
        
            sch_submitted = st.form_submit_button("Add Scholarship Application")
            if sch_submitted and university_name and course_of_study:
                add_scholarship(user_id, university_name, scholarship_type, course_of_study, application_date, deadline)
                st.success("Scholarship application added!")

    st.subheader("Your Scholarship Applications")
    scholarships = get_scholarships(user_id)
    if scholarships:
        sch_cols = ['ID', 'User ID', 'University', 'Type', 'Course', 'Applied', 'Deadline', 'Status', 'Created At']
        df_sch = pd.DataFrame(scholarships, columns=sch_cols)
        
        st.dataframe(df_sch[['University', 'Type', 'Course', 'Deadline', 'Status', 'Created At']], use_container_width=True)
        
        csv_scholarships = convert_df_to_csv(df_sch)
        st.download_button(
            label="Download Scholarships as CSV",
            data=csv_scholarships,
            file_name='scholarship_applications.csv',
            mime='text/csv',
        )
    else:
        st.info("No scholarship applications found. Add one above!")