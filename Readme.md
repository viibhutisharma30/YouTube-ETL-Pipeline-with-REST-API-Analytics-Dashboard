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
<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/7f80e1a4-32d3-4a2f-9708-4c2d6fcb2d08" />

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



