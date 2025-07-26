from flask import Flask, render_template, redirect, request, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "my_project"

@app.route("/", methods=["GET", "POST"])
def front():
    return render_template("base.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')

        if len(password) < 8:
            flash('Password must be atleast 8 characters long')
            return redirect(url_for('login_page'))

        if not name or not password:
            flash("Both name and password are required.")
            return redirect(url_for('login_page'))  

        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute('SELECT * FROM user WHERE name = ? AND password = ?', (name, password))
        user = cur.fetchone()
        con.close()

        if user:
            session['user'] = name
            return redirect(url_for('notes'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('login_page'))

    return render_template('login.html')

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        con = sqlite3.connect("database.db")
        cur = con.cursor()

        existing = cur.execute("SELECT * FROM user WHERE name = ?", (name,)).fetchone()
        if existing:
            flash("User already exists!")
            return render_template("create_account.html")

        cur.execute("INSERT INTO user (name, password) VALUES (?, ?)", (name, password))
        con.commit()
        con.close()
        flash("Account created! Please log in.")
        return redirect(url_for("login_page"))
    
    return render_template("create_account.html")

@app.route("/notes", methods=["GET", "POST"])
def notes():
    if "user" not in session:
        flash("Please log in first.")
        return redirect(url_for("login_page"))

    user = session["user"]

    if request.method == "POST":
        content = request.form.get("notes")
        if content:
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("INSERT INTO notes (username, content) VALUES (?, ?)", (user, content))
            con.commit()
            con.close()
            flash("Note saved successfully.")

    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT content FROM notes WHERE username = ?", (user,))
    notes_data = cur.fetchall()
    con.close()

    return render_template("notes.html", user=user, notes=notes_data)

@app.route("/delete_note", methods=["POST"])
def delete_note():
    if "user" not in session:
        flash("Please log in first.")
        return redirect(url_for("login_page"))

    user = session["user"]
    content = request.form.get("note_content")

    if content:
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("DELETE FROM notes WHERE username = ? AND content = ?", (user, content))
        con.commit()
        con.close()
        flash("Note deleted successfully.")

    return redirect(url_for("notes"))

@app.route("/view_users")
def view_users():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT id, name FROM user")
    users = cur.fetchall()
    con.close()
    return str(users)

@app.route("/logout")
def logout():
    session.pop("user", None)  
    flash("Logged out successfully.")
    return render_template("logout.html")

if __name__ == "__main__":
    app.run(debug=True)
