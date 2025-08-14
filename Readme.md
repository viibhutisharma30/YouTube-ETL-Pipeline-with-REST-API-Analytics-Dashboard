# 📊 YouTube Data ETL Pipeline + Analytics Dashboard

A complete **ETL pipeline** that extracts, transforms, and loads YouTube channel data into a database, and visualizes it using a Streamlit dashboard. Built with **FastAPI**, **SQLAlchemy**, and **Altair**.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Sample Outputs](#sample-outputs)
- [Future Improvements](#future-improvements)
- [License](#license)

## Features
- 🔹 **Extracts YouTube data** (videos, comments, channel stats) via YouTube Data API
- 🔹 **Transforms** raw JSON data into clean, structured tables
- 🔹 **Loads** data into SQLite database
- 🔹 **Interactive Dashboard** with:
  - Overall statistics
  - Daily upload trends
  - Top 10 videos by views
  - Video distribution by category
  - Comment sentiment analysis

## Architecture
<img width="1024" height="646" alt="Architecture" src="https://github.com/user-attachments/assets/5cd26bf4-ad62-406f-9183-95689ac44543" />

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy
- **Database:** SQLite
- **Dashboard:** Streamlit, Altair
- **Data Source:** YouTube Data API v3
- **Language:** Python 3.x

## Setup Instructions

1️⃣ Clone the repo
```bash
git clone https://github.com/your-username/youtube-etl-dashboard.git
cd youtube-etl-dashboard
Setup Instructions
```

2️⃣ Create a virtual environment & install dependencies
```bash
python -m venv venv
# On Mac/Linux
source venv/bin/activate
# On Windows
venv\Scripts\activate

pip install -r requirements.txt
```
3️⃣ Set up your .env file
```bash
Create a file named .env in the project root and add:

YOUTUBE_API_KEY=your_api_key_here
```
4️⃣ Run the ETL process
```bash
python src/run_etl.py
```
5️⃣ Start the FastAPI backend
```bash
uvicorn api.main:app --reload
```
6️⃣ Start the Streamlit dashboard
```bash
streamlit run dashboard/app.py
```
## Usage

After starting both backend and frontend, open:

📍 Dashboard: http://localhost:8501  
📍 API Docs: http://localhost:8000/docs  

### Dashboard Preview
<img width="1908" height="907" alt="image" src="https://github.com/user-attachments/assets/134e9ded-4b43-419e-b0a0-c1dca130e79b" />

## Project Structure
```bash
├── api/
│ └── main.py # FastAPI backend providing endpoints to query processed data
├── dashboard/
│ └── app.py # Streamlit dashboard for interactive visualizations and insights
├── queries/
│ └── analytics.sql # Predefined SQL queries used by API and dashboard
├── src/
│ ├── extract.py # Extract: YouTube API data extraction
│ ├── transform.py # Transform: Data cleaning, standardization, enrichment
│ ├── load.py # Load: Load transformed data into SQLite (youtube.db)
│ ├── run_etl.py # ETL orchestration script calling extract, transform, and load
│ ├── check_db.py # Utility to check database connection and tables
│ └── config.py # Configuration file storing API keys and settings
├── data/
│ └── youtube.db # SQLite database storing videos, channels, comments
├── requirements.txt
├── README.md
└── .gitignore
```
##Sample output
<img width="1908" height="907" alt="image" src="https://github.com/user-attachments/assets/134e9ded-4b43-419e-b0a0-c1dca130e79b" />
<img width="1665" height="654" alt="image" src="https://github.com/user-attachments/assets/9151c03f-84d5-4038-a2df-a51322be6f55" />
<img width="1660" height="677" alt="image" src="https://github.com/user-attachments/assets/43b4a71d-1a47-4b90-9611-aa9312f57350" />
<img width="1613" height="597" alt="image" src="https://github.com/user-attachments/assets/d9869f49-98ea-4c09-a902-7aa6345576a0" />


