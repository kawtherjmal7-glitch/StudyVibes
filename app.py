from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "studyvibe.db"


# =========================
# DATABASE
# =========================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()

    # =========================
    # STUDY PARTNER POSTS
    # =========================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            space TEXT DEFAULT 'general'
        )
    """)

    # Add space column if old database doesn't have it
    columns = [
        row["name"]
        for row in conn.execute("PRAGMA table_info(posts)").fetchall()
    ]

    if "space" not in columns:
        conn.execute(
            "ALTER TABLE posts ADD COLUMN space TEXT DEFAULT 'general'"
        )


    # =========================
    # REQUESTS
    # =========================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            sender_name TEXT NOT NULL,
            sender_email TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    """)


    # =========================
    # MESSAGES
    # =========================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_email TEXT NOT NULL,
            receiver_email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)


    # =========================
    # STUDENT TIPS
    # =========================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tip TEXT NOT NULL,
            space TEXT NOT NULL
        )
    """)


    conn.commit()
    conn.close()


# =========================
# MAIN PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# GIRLS SPACE
# =========================

@app.route("/girls")
def girls():

    conn = get_db()

    posts = conn.execute("""
        SELECT *
        FROM posts
        WHERE space = 'girls'
        ORDER BY id DESC
    """).fetchall()

    tips = conn.execute("""
        SELECT *
        FROM tips
        WHERE space = 'girls'
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "girls.html",
        posts=posts,
        tips=tips
    )


# =========================
# BOYS SPACE
# =========================

@app.route("/boys")
def boys():

    conn = get_db()

    posts = conn.execute("""
        SELECT *
        FROM posts
        WHERE space = 'boys'
        ORDER BY id DESC
    """).fetchall()

    tips = conn.execute("""
        SELECT *
        FROM tips
        WHERE space = 'boys'
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "boys.html",
        posts=posts,
        tips=tips
    )


# =========================
# GAMES
# =========================

@app.route("/games")
def games():
    return render_template("games.html")


# =========================
# STUDY PARTNER PAGE
# =========================

@app.route("/study-partner")
def study_partner():

    conn = get_db()

    posts = conn.execute("""
        SELECT *
        FROM posts
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "study_partner.html",
        posts=posts
    )


# =========================
# CREATE STUDY PARTNER POST
# =========================

@app.route("/create-post", methods=["POST"])
def create_post():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    # Detect Girls / Boys automatically
    # from the page where the form was submitted

    referrer = request.referrer or ""

    if "/girls" in referrer:
        space = "girls"

    elif "/boys" in referrer:
        space = "boys"

    else:
        space = "general"


    if name and email and subject and message:

        conn = get_db()

        conn.execute("""
            INSERT INTO posts
            (name, email, subject, message, space)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            email,
            subject,
            message,
            space
        ))

        conn.commit()
        conn.close()


    # Return to the correct Space

    if space == "girls":
        return redirect(url_for("girls"))

    elif space == "boys":
        return redirect(url_for("boys"))

    return redirect(url_for("study_partner"))


# =========================
# SEND STUDY PARTNER REQUEST
# =========================

@app.route("/send-request/<int:post_id>", methods=["POST"])
def send_request(post_id):

    sender_name = request.form.get(
        "sender_name", ""
    ).strip()

    sender_email = request.form.get(
        "sender_email", ""
    ).strip()


    if sender_name and sender_email:

        conn = get_db()

        conn.execute("""
            INSERT INTO requests
            (post_id, sender_name, sender_email)
            VALUES (?, ?, ?)
        """, (
            post_id,
            sender_name,
            sender_email
        ))

        conn.commit()
        conn.close()


    referrer = request.referrer or ""

    if "/girls" in referrer:
        return redirect(url_for("girls"))

    if "/boys" in referrer:
        return redirect(url_for("boys"))

    return redirect(url_for("study_partner"))


# =========================
# CHAT
# =========================

@app.route("/chat")
def chat():

    receiver_email = request.args.get(
        "receiver_email", ""
    ).strip()

    sender_email = request.args.get(
        "sender_email", ""
    ).strip()


    if not receiver_email or not sender_email:
        return redirect(url_for("study_partner"))


    conn = get_db()

    messages = conn.execute("""
        SELECT *
        FROM messages
        WHERE
            (sender_email = ?
             AND receiver_email = ?)
        OR
            (sender_email = ?
             AND receiver_email = ?)

        ORDER BY id ASC
    """, (
        sender_email,
        receiver_email,
        receiver_email,
        sender_email
    )).fetchall()

    conn.close()


    return render_template(
        "chat.html",
        messages=messages,
        sender_email=sender_email,
        receiver_email=receiver_email
    )


# =========================
# SEND MESSAGE
# =========================

@app.route("/send-message", methods=["POST"])
def send_message():

    sender_email = request.form.get(
        "sender_email", ""
    ).strip()

    receiver_email = request.form.get(
        "receiver_email", ""
    ).strip()

    message = request.form.get(
        "message", ""
    ).strip()


    if sender_email and receiver_email and message:

        conn = get_db()

        conn.execute("""
            INSERT INTO messages
            (sender_email, receiver_email, message)
            VALUES (?, ?, ?)
        """, (
            sender_email,
            receiver_email,
            message
        ))

        conn.commit()
        conn.close()


    return redirect(
        url_for(
            "chat",
            sender_email=sender_email,
            receiver_email=receiver_email
        )
    )


# =========================
# ALL MESSAGES
# =========================

@app.route("/messages")
def messages():

    conn = get_db()

    all_messages = conn.execute("""
        SELECT *
        FROM messages
        ORDER BY id ASC
    """).fetchall()

    conn.close()

    return render_template(
        "messages.html",
        messages=all_messages
    )


# =========================
# ADD STUDENT TIP
# =========================

@app.route("/add-tip", methods=["POST"])
def add_tip():

    name = request.form.get(
        "name", ""
    ).strip()

    tip = request.form.get(
        "tip", ""
    ).strip()

    space = request.form.get(
        "space", ""
    ).strip().lower()


    # Security / validation

    if space not in ["girls", "boys"]:
        space = "general"


    if name and tip:

        conn = get_db()

        conn.execute("""
            INSERT INTO tips
            (name, tip, space)
            VALUES (?, ?, ?)
        """, (
            name,
            tip,
            space
        ))

        conn.commit()
        conn.close()


    # Return to correct Space

    if space == "girls":
        return redirect(url_for("girls"))

    if space == "boys":
        return redirect(url_for("boys"))

    return redirect(url_for("home"))


# =========================
# START DATABASE
# =========================

init_db()


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(
        debug=True
    )