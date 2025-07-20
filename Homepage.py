from dotenv import load_dotenv
load_dotenv() 

import streamlit as st
from business_layer import register_user, verify_user 
from data_base import create_tables

# --- Page Configuration ---
st.set_page_config(
    page_title="Welcome - Application Tracker",
    page_icon="assets/grad.png",
    layout="centered"
)

# --- Initialize Database ---
create_tables()

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
h1 {
    font-weight: 700;
    color: var(--primary-color);
    text-align: center;
    padding-bottom: 0.5rem;
}
h2, h3, h4 {
    color: var(--primary-color);
    font-weight: 500;
}

/* --- Main Containers & Cards --- */
[data-testid="stForm"] {
    background-color: var(--card-background-color);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 8px 24px rgba(149, 157, 165, 0.2);
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
    font-size: 1rem;
    transition: all 0.3s ease-in-out;
    width: 100%;
}
div.stButton > button:hover {
    background-color: #1e3a5f; /* Darker blue on hover */
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
    transition: all 0.2s ease;
}
div.stTextInput > div > div > input:focus, .stDateInput > div > div > input:focus {
    border-color: var(--accent-color);
    box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2);
}

/* --- Logo Styling --- */
.logo-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    padding: 1rem 0 2rem 0;
}
.logo-container img {
    max-height: 50px;
    width: auto;
    filter: grayscale(50%);
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

# --- Page Content ---
st.title("🚀 Application Tracker")
# --- Logo Container ---
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
col1_img, col2_img, col3_img = st.columns(3)
with col1_img:
    st.image("assets/Federal-Government-3MTT-Programme.jpg")
with col2_img:
    st.image("assets/grad.png")
with col3_img:
    st.image("assets/Ai_guy.jpg")
st.markdown('</div>', unsafe_allow_html=True)

# --- UPDATED Login and Registration Forms ---
col1, col2 = st.columns(2)

with col1:
    with st.form("login_form"):
        st.subheader("Login")
        fellow_id_login = st.text_input("Enter your Fellow ID")
        password_login = st.text_input("Password", type="password") # New password field
        login_submitted = st.form_submit_button("Login")

        if login_submitted and fellow_id_login and password_login:
            # UPDATED: Use verify_user for secure login
            user_data = verify_user(fellow_id_login, password_login)
            if user_data:
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = user_data[0]
                st.session_state['fellow_id'] = user_data[1]
                st.session_state['full_name'] = user_data[2]
                st.success(f"Welcome back, {user_data[2]}!")
                st.info("Click on 'Tracker' in the sidebar to manage your applications.")
            else:
                st.error("Invalid Fellow ID or password.")

with col2:
    with st.form("registration_form"):
        st.subheader("Register")
        fellow_id_reg = st.text_input("Fellow ID")
        full_name_reg = st.text_input("Full Name")
        email_reg = st.text_input("Email")
        password_reg = st.text_input("Create a Password", type="password") # New password field
        reg_submitted = st.form_submit_button("Register")

        if reg_submitted and fellow_id_reg and full_name_reg and password_reg:
            # UPDATED: Pass password to register_user function
            user_id = register_user(fellow_id_reg, full_name_reg, email_reg, password_reg)
            if user_id:
                st.success(f"Registration successful, {full_name_reg}! You can now log in.")
            else:
                st.error("This Fellow ID might already be registered.")

# --- Sidebar (no changes) ---
st.sidebar.image("assets/profile.png", width=100)
st.sidebar.info("This is a multi-page applications app. Once logged in, navigate using the sidebar.")