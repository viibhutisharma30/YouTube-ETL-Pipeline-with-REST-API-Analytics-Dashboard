-- -- Search by keyword (to be used with LIKE in FastAPI)

-- 1. Top 10 recently published videos
SELECT * FROM videos ORDER BY publishedAt DESC LIMIT 10;

-- 2. Average view count per channel
SELECT AVG(view_count) AS avg_views FROM channels;

-- 3. Daily upload trends
SELECT DATE(published_at) AS day, COUNT(*) AS uploads
FROM videos
GROUP BY day
ORDER BY day;

-- 4. Search by keyword (example: FastAPI route will plug in the keyword)
SELECT * FROM videos WHERE title LIKE '%your_keyword%';