
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_paginate import Pagination, get_page_parameter
from flask_bootstrap import Bootstrap
import json
import pymysql
from flaskext.mysql import MySQL
import pymysql.cursors
import mysql.connector
import re
pymysql.install_as_MySQLdb()
from collections import Counter
import datetime
from statistics import mode

'''Read data from Json File'''
f = open('static/movies.json', encoding="utf8")
Movies = json.loads(f.read())

# Initialize
app = Flask(__name__)
bootstrap = Bootstrap(app)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'Flask%Crud#Application'

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = "localhost"
# app.config['MYSQL_DATABASE_PORT'] = 3308
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'movies'

# Users:
# Username: groot Password: 1234

# Intialize MySQL
mysql.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return redirect(url_for('movies'))

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if user exists using MySQL
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # Fetch one record and return result
        user = cursor.fetchone()
        # return str(user)
        # If user exists in users table in out database
        if user and check_password_hash(user[5], password):
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[4]
            # Redirect to home page
            return redirect(url_for('movies'))
        else:
            # user doesnt exist or username/password incorrect
            msg = 'Incorrect username or password!'

    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        last = request.form['last_name']
        first = request.form['first_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        hash = generate_password_hash(password)

        # Check if user exists using MySQL
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        # If user exists show error and validation checks
        if user:
            msg = 'User already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # user doesnt exists and the form data is valid, now insert new user into users table
            cursor.execute('INSERT INTO users (firstname, lastname, email, username, password) VALUES (%s,%s,%s,%s,%s)',
                           (first, last, email, username, hash,))
            conn.commit()
            msg = 'You have successfully registered!'
            return render_template('index.html')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/movies', methods=['GET', 'POST'])
def movies():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        # Get form data
        sort = request.form.get("sort")
        layout = request.form.get("page_layout")
        keyword = request.form.get("search")

        # Check if there is filter data specified by a user else use default filters
        # Redirect to movie function with filters
        if layout or keyword:
            return redirect(url_for('movie', key=sort, layout=layout, query=keyword))
        else:
            return redirect(url_for('movie', key="latest", layout=10, query=""))

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


def search(query):
    # Initialize a search list
    search_results = []
    if query:  # If there is query specified by a user, perform the search logic
        # each_movie is the dictionary that contains information of each movie
        for each_movie in Movies:
            # Loop through each key in a each_movie dictionary
            for each_key in each_movie:
                # First, search the title and year
                if each_key == "title" or each_key == "year":
                    # Convert strings to lower case using casefold(), and then check if they contain the query
                    # using the find function (if index >= 0, the title or year contains the query)
                    if str(each_movie[each_key]).casefold().find(query.casefold()) >= 0:
                        # Add movie to the search list using the list append method
                        search_results.append(each_movie)
                # Second, search the cast or genres
                elif each_key == "cast" or each_key == "genres":
                    # Continue the logic only if there is at least one element in the cast or genres array
                    if len(each_movie[each_key]) > 0:
                        # Loop through each element of the cast or genres array
                        for each_string in each_movie[each_key]:
                            # Check if an element of cast or genres array contains the query
                            # Always use casefold() for searching
                            if str(each_string).casefold().find(query.casefold()) >= 0:
                                # Add the movie to the search list if the cast of genres contains the query
                                search_results.append(each_movie)
    return search_results


@app.route('/movie')
def movie():
    if 'loggedin' in session:
        # Use the get_page_parameter of flask-paginate extension to navigate to that page number
        page = request.args.get(get_page_parameter(), type=int, default=1)

        # Get parameters (key, layout and query) from the url
        value = request.args.get('key')
        layout = request.args.get('layout')
        query = request.args.get('query')

        search_results = search(query)
        # Insert keywords into database
        conn = mysql.connect()
        cursor = conn.cursor()

        if query:            
            day = datetime.datetime.now().strftime("%A")
            for each_movie in search_results:
                for each_key in each_movie:
                    if each_key == "title":
                            cursor.execute('INSERT INTO searched (username, keywords, title, day) VALUES (%s, %s, %s, %s)',(session['username'], query, each_movie[each_key],day))
                            conn.commit()
            for each_movie in search_results:
                for each_key in each_movie:
                        if each_key == "genres":
                            genres = each_movie[each_key]
                            # return str(len(genres)) #2
                            for x in genres:
                                cursor.execute('INSERT INTO genres (username, genres, day) VALUES (%s, %s, %s)',(session['username'],x,day))
                                conn.commit()

        # Sort Movies according to the sort option
        if value == 'latest':
            sorted_list = sorted(Movies, key=lambda sort: sort['year'], reverse=True)
        elif value == 'oldest':
            sorted_list = sorted(Movies, key=lambda sort: sort['year'])
        else:
            sorted_list = sorted(Movies, key=lambda sort: sort['title'])

        # Compute the starting index for each page; index = 0 on page 1, index = 10 on page 2, etc.
        # The layout parameter in the url will be a string; Convert it to an integer to use it in an expression
        index = (page - 1) * int(layout)

        # If there is a query from a user
        if query:
            # Pagination: Extract the list of movies to be displayed on the current page using the index
            # Pagination: Display movies from 1 to 10 on page 1, movies from 10 to 20 on page 2, etc
            list_per_page = search_results[index:index + int(layout)]
            pagination = Pagination(page=page, per_page=int(layout), css_framework='bootstrap4',
                                    total=len(search_results),
                                    record_name='Movies')
        # If no query, then apply the sort and layout filters
        else:
            list_per_page = sorted_list[index:index + int(layout)]
            pagination = Pagination(page=page, per_page=int(layout), css_framework='bootstrap4', total=len(sorted_list),
                                    record_name='Movies')
        # Render the html page to display movies along with the pagination
        return render_template('movies.html', movies=list_per_page, pagination=pagination)

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/history')
def history():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the user info for the user so we can display it on the profile page
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(DISTINCT keywords) FROM searched WHERE username = %s', (session['username'],))
        user = cursor.fetchone()
        cursor.close        
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT (keywords) FROM searched WHERE username = %s', (session['username'],))
        # SELECT DISTINCT(keywords) FROM searched WHERE username = 'groot29';
        keywords = cursor.fetchall()
        # print("keywords: "+keywords)

        number_of_keywords = user[0]
        user_list = [session['username'], number_of_keywords] 

        return render_template('history.html', ulist=user_list,keywords=keywords)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/recent-searches')
def recent_searches():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the user info for the user so we can display it on the profile page
        conn = mysql.connect()        
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT (keywords) FROM searched WHERE username = %s', (session['username'],))
        keywords = cursor.fetchall()

        cursor.execute('SELECT genres FROM `genres` WHERE username = %s' , (session['username'],))
        allgenres = cursor.fetchall()
        allgenres = list(allgenres)
        counts = Counter(allgenres)
        counts_dict = dict(counts)
        # return str(counts_dict)
        Action =  counts_dict.get(('Action',))
        Thriller =  counts_dict.get(('Thriller',))
        Drama =  counts_dict.get(('Drama',))
        Western =  counts_dict.get(('Western',))
        Adventure =  counts_dict.get(('Adventure',))
        Crime =  counts_dict.get(('Crime',))
        Romance =  counts_dict.get(('Romance',))
        War =  counts_dict.get(('War',))
        Musical =  counts_dict.get(('Musical',))
        Comedy =  counts_dict.get(('Comedy',))
        Science_Fiction =  counts_dict.get(('Science Fiction',))
        Mystery =  counts_dict.get(('Mystery',))
        Disaster =  counts_dict.get(('Disaster',))
        Biography =  counts_dict.get(('Biography',))
        Animated =  counts_dict.get(('Animated',))
        Family =  counts_dict.get(('Family',))
        Fantasy =  counts_dict.get(('Fantasy',))
        Horror =  counts_dict.get(('Horror',))
        Teen =  counts_dict.get(('Teen',))
        Sports =  counts_dict.get(('Sports',))
        Short =  counts_dict.get(('Short',))
        Documentary =  counts_dict.get(('Documentary',))
        Superhero =  counts_dict.get(('Superhero',))
        Spy =  counts_dict.get(('Spy',))
        
        return render_template('recent_searches.html', keywords=keywords,Action=Action,Thriller=Thriller,Drama=Drama,Western=Western,Adventure=Adventure,Crime=Crime,Romance=Romance,War=War,Musical=Musical,Comedy=Comedy,Science_Fiction=Science_Fiction,Mystery=Mystery,Disaster=Disaster,Biography=Biography,Animated=Animated,Family=Family,Fantasy=Fantasy,Horror=Horror,Teen=Teen,Sports=Sports,Short=Short,Documentary=Documentary,Superhero=Superhero,Spy=Spy)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/watched", methods=['POST'])
def watched():
    if request.method=="POST":
        title = request.form.get("watched")
        day = datetime.datetime.now().strftime("%A")
        time = datetime.datetime.now().strftime("%H:%M:%S")
        username = session['username']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO watched (username, title, date, day, time) VALUES (%s, %s,NULL, %s, %s)',(username, title, day,time))
        conn.commit()
        return redirect(url_for('movies'))

@app.route('/recommended-movies', methods=['GET', 'POST'])
def recommended_movies():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        # Get form data
        sort = request.form.get("sort")
        layout = request.form.get("page_layout")
        # keyword = request.form.get("search")

        # Check if there is filter data specified by a user else use default filters
        # Redirect to movie function with filters
        if sort and layout:
            return redirect(url_for('recommended_movie', key=sort, layout=layout,))
        else:
            return redirect(url_for('recommended_movie', key="latest", layout=10,))

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


def recomends(genre):
    # Initialize a search list
    search_results = []
    if genre:  # If there is query specified by a user, perform the search logic
        # each_movie is the dictionary that contains information of each movie
        for each_movie in Movies:
            # Loop through each key in a each_movie dictionary
            for each_key in each_movie:
                # First, search the title and year
                if each_key == "genres":
                    # Convert strings to lower case using casefold(), and then check if they contain the query
                    # using the find function (if index >= 0, the title or year contains the query)
                    if str(each_movie[each_key]).casefold().find(genre.casefold()) >= 0:
                        # Add movie to the search list using the list append method
                        search_results.append(each_movie)
                # Second, search the cast or genres
                
    return search_results


@app.route('/recommended-movie')
def recommended_movie():
    if 'loggedin' in session:
        username = session['username']
        day = datetime.datetime.now().strftime("%A")
        conn = mysql.connect()
        cursor = conn.cursor()
        # cursor.execute('SELECT DISTINCT (genres) FROM genres WHERE username = %s and day=%s', (username,day))
        cursor.execute('SELECT genres FROM genres WHERE username = %s and day=%s', (username,day))
        genres = cursor.fetchall()
        # In today_genres we have fetched a list of all genres searched by the user on todays day from the db  
        today_genres=[]
        for x in genres:
            today_genres.append(x[0])
        if not today_genres:
            return render_template("norecommends.html")
        else:                
            # Now we will select the most searched genre of today day 
            def most_frequent(List):
                counter = 0
                num = List[0]        
                for i in List:
                    curr_frequency = List.count(i)
                    if(curr_frequency> counter):
                        counter = curr_frequency
                        num = i    
                return num
            genre=most_frequent(today_genres)

            # Use the get_page_parameter of flask-paginate extension to navigate to that page number
            page = request.args.get(get_page_parameter(), type=int, default=1)

            # Get parameters (key, layout and query) from the url
            value = request.args.get('key')
            layout = request.args.get('layout')
            # query = request.args.get('query')

            search_results = recomends(genre)

            # Sort Movies according to the sort option
            if value == 'latest':
                sorted_list = sorted(search_results, key=lambda sort: sort['year'], reverse=True)
            elif value == 'oldest':
                sorted_list = sorted(search_results, key=lambda sort: sort['year'])
            else:
                sorted_list = sorted(search_results, key=lambda sort: sort['title'])

            index = (page - 1) * int(layout)
            list_per_page = sorted_list[index:index + int(layout)]
            pagination = Pagination(page=page, per_page=int(layout), css_framework='bootstrap4',
                                    total=len(search_results),
                                    record_name='Movies')
            # Render the html page to display movies along with the pagination
            return render_template('recommended-movies.html', movies=list_per_page, pagination=pagination)

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))





if __name__ == "__main__":
    app.run()
