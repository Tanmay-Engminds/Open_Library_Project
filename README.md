**Overview** <br>
This project builds a complete data pipeline to fetch, clean, store, and visualize information about the top 100 fiction books from the Open Library API.
The system is designed using object-oriented principles, where each component has a clear and independent responsibility.<br>
**Features**
* Fetches fiction book data from the Open Library public API
* Cleans and normalizes raw API data
* Stores cleaned data in an SQL database
* Visualizes publication trends over time <br>
**API Used**
```bash
https://openlibrary.org/search.json
```
---
## BookFetcher
**Responsibility:**  
Fetching raw book data from the Open Library API.
**Data Retrieved:**
* Title
* Authors
* First publish year
---

## BookCleaner
**Responsibility:**  
Prepare raw data for analysis and storage.
**Cleaning Steps:**
* Removes books with missing titles
* Converts author lists into readable strings
* Converts publish year to numeric format
* Removes incomplete records, duplicate entries
---

## BookDatabase
**Responsibility:**  
Store and retrieve cleaned data using SQL and storing in SQLite.

---

## BookVisualizer
**Responsibility:**  
Analyze and visualize book publication trends.
**Visualization:**
* Bar plot of number of fiction books by first publish year
