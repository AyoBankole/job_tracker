# 🚀 Professional Job & Scholarship Application Tracker

A sophisticated, multi-page Streamlit application designed to help users efficiently track their job and scholarship applications. This tool is built for cloud deployment and features a modern, clean user interface.

<!-- Optional: Add a screenshot of your app later -->

## ✨ Key Features

* **Secure User Authentication:** A robust registration and login system using a unique `Fellow ID`.

* **Multi-Page Interface:** A dedicated login/registration page and a separate, full-featured dashboard for tracking applications.

* **Dual Tracking:** Add, view, and manage both job and scholarship applications in separate, organized sections.

* **Automated In-App Reminders:** Automatically receive on-screen notifications for scholarship deadlines that are approaching within the next 7 days.

* **Data Export:** Download your job or scholarship application data to a CSV file with a single click.

* **Cloud-Ready Database:** Utilizes PostgreSQL, making it perfect for deployment on platforms like Render.

* **Modern UI/UX:** A professional "Midnight Blue" theme with a focus on readability and ease of use.

## 🛠️ Technologies Used

* **Backend:** Python

* **Web Framework:** Streamlit

* **Database:** PostgreSQL

* **Python Libraries:**

  * `psycopg2-binary` for PostgreSQL connection.

  * `pandas` for data manipulation.

  * `python-dotenv` for managing environment variables.

## 📂 Project Structure

The project is organized into a modular and scalable structure, ideal for a multi-page Streamlit application.

```
job_scholarship_tracker/
│
├── assets/
│   └── (Your images: profile.png, grad.png, etc.)
│
├── pages/
│   └── 1_Tracker.py        # The main dashboard page
│
├── .gitignore              # Specifies files for Git to ignore
├── business_layer.py       # Handles core application logic
├── config.py               # Manages configuration (e.g., database URL)
├── data_base.py            # Handles database connection and setup
├── main_app.py             # The login and registration page
└── requirements.txt        # Lists project dependencies

```

## ⚙️ Local Setup and Installation

Follow these steps to run the application on your local machine.

### 1. Prerequisites

* Python 3.8+

* Git

* A free PostgreSQL database (e.g., from [Render](https://render.com/))

### 2. Clone the Repository

```
git clone [https://github.com/AyoBankole/job_tracker.git](https://github.com/AyoBankole/job_tracker.git)
cd job_tracker

```

### 3. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

```

### 4. Install Dependencies

Install all the required packages using the `requirements.txt` file.

```
pip install -r requirements.txt

```

### 5. Configure Environment Variables

The application requires a database URL to connect to.

* Create a file named `.env` in the root of your project folder.

* Add the following line to it, replacing the placeholder with your **External Connection URL** from your PostgreSQL provider.

  * **Important:** Add `?sslmode=require` to the end of your URL.

```
DATABASE_URL="postgres://user:password@external-host.com/database_name?sslmode=require"

```

* Ensure your `.gitignore` file contains `.env` to keep your database credentials secure.

### 6. Run the Application

The `create_tables()` function will run automatically on the first start to set up your database schema.

```
streamlit run main_app.py

```

Open your browser and navigate to `http://localhost:8501`.

## ☁️ Deployment on Render

This application is optimized for deployment on a platform like Render.

1. **Push to GitHub:** Ensure your latest code is pushed to your GitHub repository.

2. **Create a Web Service:** On the Render dashboard, create a new **Web Service** and connect it to your GitHub repository.

3. **Configure Settings:**

   * **Runtime:** `Python 3`

   * **Build Command:** `pip install -r requirements.txt`

   * **Start Command:** `streamlit run main_app.py`

4. **Add Environment Variable:**

   * Go to the **Environment** tab for your new web service.

   * Add a new environment variable:

     * **Key:** `DATABASE_URL`

     * **Value:** Paste your **Internal Connection URL** from your Render PostgreSQL database, making sure to add `?sslmode=require` to the end.

5. **Deploy:** Click "Create Web Service". Render will build and deploy your application.

## 🚀 How to Use the App

1. **Register:** On the main page, fill in your `Fellow ID`, `Full Name`, and `Email` in the registration form.

2. **Login:** Use your unique `Fellow ID` to log in.

3. **Navigate:** Once logged in, use the sidebar to navigate to the **Tracker** page.

4. **Add Applications:** Use the "Add a New Job/Scholarship Application" sections to enter your data.

5. **View & Export:** Your applications will appear in tables. Use the "Download as CSV" button to export your data.

6. **Get Reminders:** The app will automatically show you alerts for any scholarship deadlines that are 7 days away or less.

## ✍️ Author

* **AyoBankole** - [GitHub Profile](https://github.com/AyoBankole)

## 📜 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
