from dbCode import *
''''
# Code from Project Introductory Slides
# get items_list
items_list = get_list_of_dictionaries(category)
return render_template('display_items.html', items = items_list)

from decimal import Decimal
import ast
@app.route('/access_granted', methods=['GET', 'POST'])
def access_granted():
    if request.method == 'POST':
        selected_item = request.form.get('selected_item')
        
        selected_item_dict = ast.literal_eval(selected_item)
        #Convert float values to Decimal
        for key, value in selected_item_dict.items():
            if isinstance(value, float):
                selected_item_dict[key] = Decimal(str(value))
                
from flask import session

@app.route('/log-in-user', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Extract form data
        name = request.form['name']
        session['username'] = name
        
@app.route('/display-user-stats')
def user-stats():
    key = {"Name":session['username']}
    response = table.get_item(Key=key)'''

# Took this code from previous classes and lab
from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        genre = request.form['genre']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name:", name, ":", "Favorite Genre:", genre)
        
        flash('User added successfully!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')


@app.route('/display-users')
def display_users():
    # hard code a value to the users_list;
    # note that this could have been a result from an SQL query :) 
    users_list = (('John','Doe','Comedy'),('Jane', 'Doe','Drama'))
    return render_template('display_users.html', users = users_list)

@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name to Delete:", name)
        
        flash('User deleted successfully!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_user.html')
        
# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

