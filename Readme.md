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
<img width="843" height="684" alt="image" src="https://github.com/user-attachments/assets/ce2f081b-c186-4edc-a703-78f350705acc" />
