# 🚀 Job & Scholarship Application Tracker 📝

## Overview

This application is a Streamlit-based tool designed to help users track their job and scholarship applications efficiently. It allows users to register 👤, log in 🔑, add new applications ➕, and set reminders ⏰ for important deadlines or interview dates. The application features a user-friendly interface with a custom theme inspired by SDG8 (Decent Work and Economic Growth) 🌱.

## Key Features

* **User Registration:** New users can register their details through a sidebar form. ✅
* **Dashboard Login:** Registered users can log in using their email to access their application tracking dashboard. 🚪
* **Job Application Tracking:** Users can add and view their job applications, including company name, job title, and application date. 💼
* **Scholarship Application Tracking:** Users can add and view their scholarship applications, including scholarship name, application date, and deadline. 🎓
* **Reminders:** Users can set reminders for specific application IDs with a date and message. 🔔
* **Database Integration:** The application interacts with a database (defined in `data_base.py`) to store and retrieve user and application data. 💾
* **Custom Theming:** The application is styled with a custom CSS theme that incorporates the color palette of SDG8, providing a visually appealing and relevant user experience. 🎨
* **Responsive Design:** Built with Streamlit, the application offers a responsive layout that adapts to different screen sizes.📱

## Technologies Used

* **Python:** 🐍 The primary programming language used.
* **Streamlit:** 🌊 A Python library used to create the web application interface.
* **datetime:** 🗓️ A Python module for working with dates.
* **Custom Modules:**
    * `business_layer.py`: ⚙️ Contains functions for handling the business logic of the application (e.g., registering users, adding applications).
    * `data_base.py`: 📦 Contains functions for interacting with the database (e.g., creating connections, creating tables).

## Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2.  **Install required Python packages:**
    Ensure you have Python installed on your system. Then, install the necessary libraries using pip:
    ```bash
    pip install streamlit
    # Assuming your business_layer and data_base modules might have other dependencies, install them as well.
    # For example, if you are using SQLite, you might not need to install anything extra.
    # If you are using other databases like PostgreSQL or MySQL, you'll need their respective Python drivers.
    # Example for PostgreSQL: pip install psycopg2-binary
    # Example for MySQL: pip install mysql-connector-python
    ```
    **Note:** Replace `<repository_url>` with the actual URL of your project repository.

3.  **Set up the database:**
    Ensure that your database is set up and accessible. The `data_base.py` module likely contains the logic to create the database and tables if they don't exist. You might need to configure the database connection details within `data_base.py`. 🛠️

## Usage

1.  **Run the Streamlit application:**
    Navigate to the directory containing the main Python script (the one provided in the code block) and run the following command in your terminal:
    ```bash
    streamlit run your_script_name.py
    ```
    Replace `your_script_name.py` with the actual name of your Python file. ▶️

2.  **Access the application in your browser:**
    Streamlit will automatically open a new tab in your web browser with the application running. The URL will typically be `http://localhost:8501`. 🌐

3.  **User Registration:**
    * On the sidebar, under "User Registration", fill in the required details (Full Name, Education Level, University, Course of Study, Email). 📝
    * Click the "Register" button. ✍️
    * If successful, a confirmation message will appear on the sidebar, along with your assigned User ID. 👍

4.  **Dashboard Login:**
    * In the main section of the application, under "Dashboard", enter the email address you used during registration in the "Registered Email" field. 📧
    * The application will recognize your email and display a welcome message with your name and User ID. 👋

5.  **Tracking Job Applications:**
    * Under the "Job Applications" section, fill in the "Company Name", "Job Title", and select the "Application Date". 🏢
    * Click the "Add Job Application" button to save the entry. ✅
    * Your added job applications will be listed under the "Your Job Applications" section. 📑

6.  **Tracking Scholarship Applications:**
    * Under the "Scholarship Applications" section, fill in the "Scholarship Name", select the "Application Date", and the "Deadline". 💰
    * Click the "Add Scholarship Application" button to save the entry. ✅
    * Your added scholarship applications will be listed under the "Your Scholarship Applications" section. 📜

7.  **Setting Reminders:**
    * Under the "Reminders" section, enter the "Application ID" (the ID of the job or scholarship application you want to set a reminder for), select the "Reminder Date", and enter a "Reminder Message". 🔔
    * Click the "Add Reminder" button to save the reminder. ✅
    * Your added reminders will be listed under the "Your Reminders" section. 🗓️

## Customization

The application's appearance is customized using CSS styles defined within the Python script. These styles are themed around SDG8. You can modify the look and feel of the application by:

* **Editing the `custom_css` variable:** Change the color variables (`--sdg-primary`, `--sdg-secondary`, `--sdg-background`) or any other CSS properties to match your preferences or branding. 🎨
* **Adding more specific CSS rules:** Target specific elements or classes within the Streamlit application to apply more detailed styling. Refer to Streamlit's documentation for more information on available classes and how to inspect elements. ✨

## Project Structure

The project likely has the following structure:
