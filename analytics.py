import pandas as pd
from textblob import TextBlob
from db import get_all_movies, get_all_watch_history

def analyze_genres():
    movies = get_all_movies()
    if not movies:
        print("No movies in collection yet.")
        return

    df = pd.DataFrame(movies, columns=[
        "id", "title", "year", "genre", "duration_min", "format", "price_paid", "personal_rate"
    ])

    genre_counts = (
        df["genre"]
        .fillna("Unknown")
        .str.split(",", expand=True)
        .stack()
        .str.strip()
        .value_counts()
    )

    print("\n=== Genre Distribution (Genre: Amount) ===")
    for genre, count in genre_counts.items():
        print(f"{genre:<20} : {count}")


def analyze_rewatches():
    history = get_all_watch_history()
    if not history:
        print("No watch history yet.")
        return

    df = pd.DataFrame(history, columns=["id", "title", "date_watched", "rewatch", "note", "sentiment"])
    rewatch_counts = df.groupby("title")["rewatch"].sum().sort_values(ascending=False)

    print("\n=== Rewatch Frequency (Movie: Amount of rewatch) ===")
    for title, count in rewatch_counts.items():
        if count == 1:
            print(f"{title:<30} : {count} rewatches")
        else:
            print(f"{title:<30} : 1st watch")


def analyze_sentiment_for_notes():
    history = get_all_watch_history()
    if not history:
        print("No watch history yet.")
        return

    df = pd.DataFrame(history, columns=["id", "title", "date_watched", "rewatch", "note", "sentiment"])

    # Recalculate sentiment in case new notes were added
    df["sentiment"] = df["note"].fillna("").apply(lambda t: TextBlob(t).sentiment.polarity)

    print("\n=== Sentiment Analysis (Movie | Note | Score) ===")

    # Loop through each watch entry and print movie, note, sentiment
    for _, row in df.iterrows():
        title = row["title"]
        note = row["note"] if row["note"] else "(no note)"
        sentiment = row["sentiment"]

        # Clean formatted output
        print(f"{title:<30} | \"{note}\" | {sentiment:.4f}")



def collection_value_estimator():
    movies = get_all_movies()
    if not movies:
        print("No movies in collection yet.")
        return

    df = pd.DataFrame(movies, columns=[
        "id", "title", "year", "genre", "duration_min", "format", "price_paid", "personal_rate"
    ])

    total_value = df["price_paid"].fillna(0).sum()
    avg_price = df["price_paid"].fillna(0).mean()

    print("\n=== Collection Value ===")
    print(f"Estimated total value: {total_value:.2f}")
    print(f"Average price per movie: {avg_price:.2f}")
