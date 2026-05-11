# AutoAdept 🚗🤖

An AI-powered digital car showroom and recommendation mentor. Built with Python, Flask, Vanilla JS, and the Google Gemini API, it transforms the traditional car-buying research phase into a conversational, context-aware experience.

## ✨ Features
* **Zero-Latency Dynamic Filtering:** Instantly filter a database of 1,200+ vehicles by budget, body type, fuel, and seating capacity without page reloads.
* **Context-Aware AI Mentor:** A floating Gemini-powered chat widget that reads the exact cars currently visible on your screen to give highly specific, comparative advice.
* **Intelligent Image Radar:** A custom OS-level Python algorithm that pre-flights the local filesystem to map `.jpg` assets dynamically, completely eliminating 404 broken image errors.
* **Frictionless UI/UX:** Features shape-shifting action buttons, responsive CSS grid layouts, and dynamic DOM manipulation for lead generation modals.

## 🛠️ Tech Stack
* **Backend:** Python 3, Flask, PyMySQL
* **Frontend:** HTML5, CSS3, ES6 Vanilla JavaScript
* **Database:** MySQL 8.0
* **AI Integration:** Google Generative AI SDK (Gemini 2.5 Flash)

## 🚀 How to Run Locally

### Prerequisites
* **Python 3.8+** installed on your computer.
* **MySQL Server** installed and running locally.

### 1. Download and Extract the Project
* Click the green **"<> Code"** button at the top right of this repository.
* Select **"Download ZIP"**.
* Extract the downloaded `.zip` file to a folder on your computer.
* Open your terminal or command prompt and navigate (`cd`) into that extracted AutoAdept folder.

### 2. Set Up a Virtual Environment
It is highly recommended to run this project in an isolated virtual environment.
* **Create the environment:**
  ```bash
  python -m venv venv
* **Activate it (Windows)::**
  ```bash
  venv\Scripts\activate
* **Activate it (Mac/Linux):**
  ```bash
  source venv/bin/activate

### 3. Install Required Libraries
With your virtual environment active, install the necessary Python packages:
  ```bash
  pip install Flask PyMySQL google-generativeai pandas

### 4. Database Setup
You need to load the car data into your local MySQL server so the showroom has inventory.
* Open your MySQL Command Line or MySQL Workbench.
* Create the empty database by running:
  ```bash
  CREATE DATABASE car_mentor_db;
* Import the provided database dump file (car_mentor_db_cars.sql) into this new database to populate all the vehicle records.
* Open app.py in your code editor and update the database credentials (around line 15) to match your local MySQL setup:
  * DB_HOST = 'localhost'
  * DB_USER = 'root' (Or your MySQL username)
  * DB_PASSWORD = 'password' (Change this to your actual MySQL password)

### 5. Add Your AI API Key
* Get a free Gemini API key from Google AI Studio.
* Open app.py and paste your key into the configuration line (around line 11):
genai.configure(api_key="YOUR_API_KEY_HERE")

### 6. Start the Showroom!
Run the Flask development server:
  ```bash
  python app.py
Open your web browser and go to http://localhost:5000 to start exploring the digital showroom and chatting with the AI Mentor!
