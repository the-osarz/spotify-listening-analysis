# Spotify Listening Analysis

## Overview

Music is part of everyday life, but have you ever wondered what your listening habits look like when you examine the data?

This project explores my personal Spotify listening history to better understand my music preferences, listening patterns, and engagement over time.

I used Python to process the exported Spotify data, SQLite to organize and store the information, SQL to explore the dataset, and Power BI to build an interactive dashboard.

The project provided an opportunity to apply data analysis skills to a dataset that is both personal and familiar, while developing a clearer understanding of how raw data can be transformed into meaningful insights.

## Project Objectives

The analysis focuses on questions such as:

- Which artists do I listen to the most?
- Which songs have the highest number of streams?
- Which song accounts for the most total listening time?
- How do my listening habits change from month to month and year to year?
- Which days are associated with the highest listening activity?

These questions guided the data exploration and dashboard development.

## Tools and Technologies

| Tool | Purpose |
|---|---|
| Python | Data extraction, cleaning, and transformation |
| Pandas | Data manipulation and preparation |
| SQLite | Storing and organizing the processed data |
| SQL | Querying and exploring listening patterns |
| Power BI | Data visualization and interactive reporting |

## Project Workflow

### 1. Data Collection

I downloaded my personal listening-history data and music library information through Spotify's account data export.

### 2. Data Processing

Python was used to read and process the exported JSON files, organize the records, and prepare them for analysis.

### 3. Database Development

The processed information was stored in SQLite, with related tables covering artists, genres, albums, tracks, artist-track relationships, and streaming events.

### 4. Data Exploration

SQL queries were used to investigate listening activity, identify frequently played artists and songs, and explore patterns within the data.

### 5. Dashboard Development

Power BI was used to present the findings through visualizations, making it easier to compare listening activity and identify trends over time.

## Dashboard Insights

The Power BI dashboard explores several aspects of my listening history, including:

- Total number of listening events
- Most-streamed artist
- Most-streamed song
- Top 10 most-streamed artists
- Top 10 most-streamed songs
- Monthly and yearly listening trends
- Busiest listening day
- Song with the highest total listening time

The dashboard provides a visual overview of these metrics and makes it easier to explore how my listening habits vary.

## Repository Structure

```text
Spotify Analysis/
├── dashboard/
│   └── Spotify analytics dashboard.pbix
├── Images/
│   └── Dashboard screenshots
├── Spotify tables CSV/
│   └── Processed data tables
├── Spotify Analysis.py
└── Spotify data analysis.docx
```

*The structure above describes the main project components. Personal raw listening-history exports and private database files are excluded from the public repository.*

## Key Learning Outcomes

Through this project, I gained practical experience in:

- Working with JSON data and transforming it into structured datasets
- Using Python and Pandas for data preparation
- Designing relational database tables
- Writing SQL queries to investigate real-world data
- Connecting data sources and building visual reports in Power BI
- Translating analytical questions into measurable metrics and visual insights

## Conclusion

This project is part of my continued development in data analytics and research. It demonstrates how tools such as Python, SQL, SQLite, and Power BI can work together to turn raw data into information that is easier to understand and communicate.

Rather than simply looking at listening statistics, the project helped me approach familiar data with analytical questions and use the answers to tell a clearer story.

---

**Privacy note:** This project uses personal Spotify account data. Raw listening-history exports and other sensitive personal records are not included in the public repository.
