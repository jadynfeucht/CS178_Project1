#I used ChatGPT to help me write some of these, and to help me rearrange them in a more conceptually sound way. 
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Needed for flash messaging and sessions

### ----- HOME & INDEX ROUTES ----- ###

@app.route("/")
def index():
    countries = get_list_of_dictionaries()
    return render_template("index.html", results=countries)

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))  # ✅ Protects dashboard
    return render_template("dashboard.html", username=session["username"])

### ----- USER AUTH ROUTES ----- ###

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        travel_history = request.form['travel_history']
        travel_destination = request.form['travel_destination']

        create_user(username, password, first_name, last_name, travel_history, travel_destination)
        flash('User created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = get_users() or []  # Avoid NoneType error
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return redirect(url_for('dashboard'))  # ✅ correct behavior
        
        flash('Invalid credentials. Try again.')  # ❌ fallback for bad login
        return render_template('login.html')  # ✅ Show login form again if login fails

    return render_template('login.html')  # ✅ Show login form on GET



@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

### ----- USER CRUD ROUTES ----- ###

@app.route("/add-user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        username = request.form["username"]  # Corrected field name
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        travel_history = request.form["travel_history"]
        travel_destinations = request.form["travel_destinations"]

        # Create the user in the database
        create_user(username, password, first_name, last_name, travel_history, travel_destinations)

        flash("User added successfully!", "success")
        return redirect(url_for("index"))  # Redirecting to the index page

    return render_template("add_user.html")

def create_user(username, password, first_name, last_name, travel_history, travel_destination):
    query = """
        INSERT INTO users (username, password, first_name, last_name, travel_history, travel_destination)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    execute_query(query, (username, password, first_name, last_name, travel_history, travel_destination), fetch=False)

@app.route("/delete-user", methods=["GET", "POST"])
def delete_user():
    if request.method == "POST":
        username = request.form["name"]
        delete_user_by_name(username)
        flash(f"User '{username}' deleted successfully!", "success")
        return redirect(url_for("index"))
    return render_template("delete_user.html")

@app.route("/display-users")
def display_users():
    users = read_users()
    return render_template("display_users.html", users=users)

@app.route("/update-user/<int:user_id>", methods=["GET", "POST"])
def update_user_route(user_id):
    if request.method == "POST":
        new_first_name = request.form["first_name"]
        new_last_name = request.form["last_name"]
        new_travel_history = request.form["new_travel_history"]
        new_travel_destination = request.form["new_travel_destination"]
        update_user(user_id, new_first_name, new_last_name, new_travel_history, new_travel_destination)
        flash(f"User {new_first_name} updated successfully!", "success")
        return redirect(url_for("display_users"))
    user = read_user_by_id(user_id)[0]
    return render_template("update_user.html", user=user)

### ----- TRAVEL HISTORY ROUTES ----- ###

@app.route("/add-travel", methods=["GET", "POST"])
def add_travel():
    if request.method == "POST":
        username = request.form["username"]
        destination = request.form["destination"]
        date_of_trip = request.form["date_of_trip"]
        add_travel_history(username, destination, date_of_trip)
        flash("Travel entry added successfully!", "success")
        return redirect(url_for("dashboard"))
    return render_template("add_travel.html")


@app.route("/get-travel-history/<username>")
def get_travel_history_route(username):
    travel_history = get_travel_history(username)
    return render_template("travel_history.html", travel_history=travel_history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
