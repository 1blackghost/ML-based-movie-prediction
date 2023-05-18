import sqlite3

DATABASE_FILE = 'users.db'


def reset_back_to_start() -> None:
    """
    Reset the database to the initial state.

    This function drops the existing 'users' table and recreates it.

    Note:
        This action requires admin privilege.

    Returns:
        None
    """
    conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
    c = conn.cursor()

    print("[WARNING!] You need admin privilege to clear and reset the data! Are you sure? (y/n/yes/no)")
    a = input()
    c.execute("DROP TABLE IF EXISTS users")
    if a in ("y", "yes"):
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (uid INTEGER PRIMARY KEY AUTOINCREMENT,
                     movie_name TEXT NOT NULL,
                     progress INTEGER DEFAULT 0,
                     message TEXT,
                     sentiment TEXT
                     )''')

    conn.commit()
    conn.close()


def update_user(uid, movie_name=None, progress=None, message=None, sentiment=None) -> None:
    """
    Update user information in the database.

    Args:
        uid: User ID of the user to update.
        movie_name: New movie name (optional).
        progress: New progress (optional).
        message: New message (optional).
        sentiment: New sentiment (optional).

    Returns:
        None
    """
    conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
    c = conn.cursor()
    update_fields = []

    if movie_name is not None:
        update_fields.append(("movie_name", movie_name))
    if progress is not None:
        update_fields.append(("progress", progress))
    if message is not None:
        update_fields.append(("message", message))
    if sentiment is not None:
        update_fields.append(("sentiment", sentiment))

    if len(update_fields) > 0:
        update_query = "UPDATE users SET "
        update_query += ", ".join(f"{field} = ?" for field, _ in update_fields)
        update_query += " WHERE uid = ?"
        values = [value for _, value in update_fields]
        values.append(uid)
        c.execute(update_query, values)

    conn.commit()
    conn.close()


def insert_user(movie_name="", progress=0, message="", sentiment="") -> int:
    """
    Insert a new user into the database.

    Args:
        movie_name: Movie name.
        progress: Progress.
        message: Message.
        sentiment: Sentiment.

    Returns:
        int: ID of the inserted user.
    """
    conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
    c = conn.cursor()

    c.execute("INSERT INTO users (movie_name, progress, message, sentiment) VALUES (?, ?, ?, ?)",
              (movie_name, progress, message, sentiment))
    uid = c.lastrowid
    conn.commit()
    conn.close()

    return uid


def read_user(uid=-1) -> list:
    """
    Read user details from the database.

    Args:
        uid: User ID to retrieve. If -1, retrieve all users.

    Returns:
        list: User details as a list of tuples.
    """
    conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
    c = conn.cursor()

    if uid != -1:
        c.execute("SELECT * FROM users WHERE uid = ?", (uid,))
        result = c.fetchone()
    else:
        c.execute("SELECT * FROM users")
    conn.close()

    return result
