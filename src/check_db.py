import sqlite3

conn = sqlite3.connect("C:/Users/LENOVO/OneDrive/Desktop/Youtube ELT Pipeline/database/youtube.db")
results = conn.execute("SELECT * FROM videos LIMIT 5").fetchall()
print(results)