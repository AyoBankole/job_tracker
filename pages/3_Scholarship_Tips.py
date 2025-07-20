import streamlit as st
import random

# --- Page Configuration ---
st.set_page_config(page_title="Scholarship Tips", page_icon="💡")

# --- List of Tips ---
# You can expand this list with as many tips as you like.
scholarship_tips = [
    "Start your search early! Many scholarship deadlines are months before the academic year begins.",
    "Customize your application for each scholarship. Generic essays rarely stand out from the crowd.",
    "Proofread everything twice! Typos and grammatical errors can get your application disqualified immediately.",
    "Don't neglect smaller, local scholarships. They often have significantly less competition.",
    "Showcase your unique personality and story in your essays, not just a list of your achievements.",
    "Request strong letters of recommendation from teachers or mentors who know you well and can speak to your strengths.",
    "Highlight your volunteer work and community service to show you are a well-rounded candidate.",
    "Create a detailed timeline with all your deadlines in a calendar to stay organized and avoid last-minute stress.",
    "Never pay to apply for a scholarship. Legitimate scholarship opportunities are always free.",
    "Apply for scholarships even if you don't think you perfectly meet every single requirement. You might be surprised!"
]

# --- Page Display ---
st.title("💡 Scholarship Know-How")
st.markdown("A collection of tips to help you succeed in your scholarship search. A new tip appears each time you visit!")
st.markdown("---")

# Select and display a random tip from the list
random_tip = random.choice(scholarship_tips)

# Display the tip in a visually appealing info box
st.info(f"**Today's Tip:** {random_tip}")

# Add a button that allows the user to get a new tip by re-running the page
st.button("Show Me Another Tip")
