from db import init_db, add_movie, get_all_movies, add_watch
from analytics import (
    analyze_genres,
    analyze_rewatches,
    analyze_sentiment_for_notes,
    collection_value_estimator,
)
from textblob import TextBlob


def get_int(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_float(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_yes_no(prompt):
    while True:
        value = input(prompt).strip().lower()
        if value in ["y", "n"]:
            return value
        print("Please enter 'y' or 'n'.")


def get_menu_choice():
    while True:
        choice = input("Choose an option: ").strip()
        if choice.isdigit():
            return choice
        print("Please enter a number.")


def show_menu():
    print("\n=== Movie Collection Manager ===")
    print("1. Add movie")
    print("2. View all movies")
    print("3. Log a watch")
    print("4. Analyze genres")
    print("5. Analyze rewatch frequency")
    print("6. Analyze sentiment for notes")
    print("7. Collection value estimator")
    print("0. Exit")


def handle_add_movie():
    print("\n--- Add Movie ---")
    title = input("Title: ").strip()

    year = get_int("Year (enter 0 to skip): ")
    year = None if year == 0 else year

    genre = input("Genre(s): ").strip()

    duration = get_int("Duration (minutes, 0 to skip): ")
    duration = None if duration == 0 else duration

    fmt = input("Format (Blu-ray/DVD/Digital/etc.): ").strip()

    price = get_float("Price paid (0 to skip): ")
    price = None if price == 0 else price

    rating = get_float("Your rating (1-10, 0 to skip): ")
    rating = None if rating == 0 else rating

    add_movie(title, year, genre, duration, fmt, price, rating)
    print("Movie added.")


def handle_view_movies():
    print("\n--- Movie List ---")
    movies = get_all_movies()
    if not movies:
        print("No movies yet.")
        return

    for m in movies:
        mid, title, year, genre, duration, fmt, price, rating = m
        print(f"[{mid}] {title} ({year if year else 'N/A'}) - {genre}")
        print(
            f"   {duration or '??'} min | {fmt or 'Unknown'} | "
            f"Price: {price or 0} | Rating: {rating or 'N/A'}"
        )


def handle_log_watch():
    print("\n--- Log Watch ---")
    movies = get_all_movies()
    if not movies:
        print("No movies to log. Add a movie first.")
        return

    for m in movies:
        mid, title, year, _, _, _, _, _ = m
        print(f"[{mid}] {title} ({year if year else 'N/A'})")

    movie_id = get_int("Enter Movie ID: ")

    date_watched = input("Date watched (YYYY-MM-DD): ").strip()
    if not date_watched:
        print("Please enter a date like 2025-12-13.")
        return

    rewatch_input = get_yes_no("Is this a rewatch? (y/n): ")
    rewatch = 1 if rewatch_input == "y" else 0

    note = input("Short note about this watch (optional): ").strip()
    sentiment = TextBlob(note).sentiment.polarity if note else 0.0

    add_watch(movie_id, date_watched, rewatch, note, sentiment)
    print("Watch logged.")


def main():
    init_db()

    while True:
        show_menu()
        choice = get_menu_choice()

        if choice == "1":
            handle_add_movie()
        elif choice == "2":
            handle_view_movies()
        elif choice == "3":
            handle_log_watch()
        elif choice == "4":
            analyze_genres()
        elif choice == "5":
            analyze_rewatches()
        elif choice == "6":
            analyze_sentiment_for_notes()
        elif choice == "7":
            collection_value_estimator()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
