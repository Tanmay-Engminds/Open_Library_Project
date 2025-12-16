import requests
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# BookFetcher
class BookFetcher:
    def __init__(self, limit=100):
        self.limit = limit
        self.url = "https://openlibrary.org/search.json"
        
    def fetch(self):
        params = {
            "subject": "fiction",
            "limit": self.limit
        }
        response = requests.get(self.url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        books = []
        for item in data.get("docs", []):
            books.append({
                "title": item.get("title"),
                "authors": item.get("author_name"),
                "first_publish_year": item.get("first_publish_year")
            })
        print(f"Fetched {len(books)} books.")
        return books
        
# BookCleaner
class BookCleaner:
    def clean(self, raw_books):
        df = pd.DataFrame(raw_books)
        df = df[df["title"].notna()] # Removing books without a title
        
        df["authors"] = df["authors"].apply( # Converting list to string
            lambda a: "; ".join(a) if isinstance(a, list) else None
        )
        
        df["first_publish_year"] = pd.to_numeric(  # Converting publish year to numeric
            df["first_publish_year"], errors="coerce"
        )
        
        df = df.dropna(subset=["authors", "first_publish_year"]) # Removing rows with missing year or authors
        
        df = df.drop_duplicates(subset=["title", "authors"]) # Removing duplicates
        return df

# BookDatabase
class BookDatabase:
    def __init__(self, db_name="books.db"):
        self.engine = create_engine(f"sqlite:///{db_name}")
    def save(self, df):
        df.to_sql("fiction_books", self.engine, index=False, if_exists="replace")
    def load(self):
        return pd.read_sql("SELECT * FROM fiction_books", self.engine)

# BookVisualizer
class BookVisualizer:
    def plot_publish_years(self, df):
        df = df.sort_values("first_publish_year")
        year_counts = df["first_publish_year"].value_counts().sort_index() # Counting books per year
        plt.figure(figsize=(16, 7))
        sns.set_theme(style="whitegrid")
        sns.barplot(
            x=year_counts.index.astype(int),
            y=year_counts.values
        )
        plt.xticks(rotation=90)
        plt.xlabel("First Publish Year")
        plt.ylabel("Number of Books")
        plt.title("Fiction Books Published by Year (Top 100)")
        plt.tight_layout()
        plt.savefig("books_by_year.png", dpi=300)
        plt.show()
        print("Plot saved as books_per_year.png")

def main():
    #Fetching
    fetcher = BookFetcher(limit=100)
    raw_books = fetcher.fetch()
    #Cleaning
    cleaner = BookCleaner()
    clean_df = cleaner.clean(raw_books)
    #Saving to DB
    db = BookDatabase()
    db.save(clean_df)
    #Visualizing
    stored_df = db.load()
    visualizer = BookVisualizer()
    visualizer.plot_publish_years(stored_df)

if __name__ == "__main__":
    main()
