import sqlite3

DB_NAME = "movies.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER,
            genre TEXT,
            duration_min INTEGER,
            format TEXT,
            price_paid REAL,
            personal_rate REAL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS watch_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            date_watched TEXT NOT NULL,
            rewatch INTEGER DEFAULT 0,
            note TEXT,
            sentiment REAL,
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        );
    """)

    conn.commit()
    conn.close()

def add_movie(title, year, genre, duration_min, fmt, price_paid, personal_rate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO movies (title, year, genre, duration_min, format, price_paid, personal_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, year, genre, duration_min, fmt, price_paid, personal_rate))
    conn.commit()
    conn.close()

def get_all_movies():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, year, genre, duration_min, format, price_paid, personal_rate FROM movies")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_watch(movie_id, date_watched, rewatch, note, sentiment):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO watch_history (movie_id, date_watched, rewatch, note, sentiment)
        VALUES (?, ?, ?, ?, ?)
    """, (movie_id, date_watched, rewatch, note, sentiment))
    conn.commit()
    conn.close()

def get_all_watch_history():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT w.id, m.title, w.date_watched, w.rewatch, w.note, w.sentiment
        FROM watch_history w
        JOIN movies m ON w.movie_id = m.id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows
