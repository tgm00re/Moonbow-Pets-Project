from unittest import result
from flask_app import app
from flask import flash, session, render_template, request, redirect, jsonify
from flask_app.models import user
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import friendship

bcrypt = Bcrypt(app)



@app.route('/')
def root():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect('/home')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/home')

@app.route('/login_form', methods=['POST'])
def login_form():
    data = { "email": request.form['email']}
    user_in_db = user.User.get_by_email(data)
    if not user_in_db:
        flash("Incorrect email/password", 'login')
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Incorrect email/password", 'login')
        return redirect('/login')
    session['user_id'] = user_in_db.id
    session['user_first'] = user_in_db.first_name
    return redirect('/home')

@app.route('/register')
def register():
    if 'user_id' in session:
        return redirect('/home')
    return render_template('register.html')

    
@app.route('/register_form', methods=['POST'])
def register_form():
    req = request.form
    print("Printing req")
    print(req)
    if not user.User.validate_user(req):
        return redirect('/register')
    pw_hash = bcrypt.generate_password_hash(req['password'])
    data = {
        "first_name": req['first_name'],
        "last_name": req['last_name'],
        "username": req['username'],
        "email": req['email'],
        "password": pw_hash
    }
    if user.User.get_by_email(data):
        print("invalid email found")
        flash("Email already exists!", 'register')
        return redirect('/register')
    session['user_id'] = user.User.save(data)
    session['user_first'] = data['first_name']
    return redirect('/home')
    


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/home')
    data = {
        "id": session['user_id']
    }
    the_user = user.User.get_single(data)
    userFriends = user.User.get_user_with_friends(data).friends
    userPets = user.User.get_all_pets(data).pets #returns the user's list of pets
    return render_template('dashboard.html', user=the_user, userFriends=userFriends, userPets=userPets)

@app.route('/shop')
def shop():
    if 'user_id' not in session:
        return redirect('/home')
    idData = {
        "id": session['user_id']
    }
    userBalance = user.User.get_single(idData).funds
    return render_template('shop.html', userBalance=userBalance)

@app.route('/add_funds')
def add_funds():
    if 'user_id' not in session:
        return redirect('/home')
    idData = {
        "id": session['user_id']
    }
    userBalance = user.User.get_single(idData).funds
    return render_template("addfunds.html", userBalance=userBalance)

@app.route('/add_funds_form', methods=['POST'])
def add_funds_form():
    if 'user_id' not in session:
        return redirect('/home')
    idData = {"id": session['user_id']}
    userBalance = user.User.get_single(idData).funds
    data = {
        "id": session['user_id'],
        "newBalance": userBalance + int(request.form['amount'])
    }
    user.User.add_funds(data)
    return redirect('/shop')

@app.route('/view_profile/<int:id>')
def view_profile(id):
    if 'user_id' not in session:
        return redirect('/home')
    data = {
        "id": id
    }
    the_user = user.User.get_single(data)
    #Get friendships of the SESSION USER
    getFriendshipsData = {"id": session['user_id']}
    friendshipList = friendship.Friendship.get_friendships(getFriendshipsData)
    #Get the the user that you are VIEWING's list of friends and their pets. *** ** * ** * * ** ** * * ** * * ** * * * * ** * *
    friendPets = user.User.get_all_pets(data).pets #returns the user's list of pets
    friendFriends = user.User.get_user_with_friends(data).friends #Returns the user
    return render_template('view_profile.html', user=the_user, friendshipList=friendshipList, friendFriends=friendFriends, friendPets=friendPets)

@app.route('/display')
def display():
    return render_template('display.html')



@app.route('/kill_session')
def kill_session():
    session.clear()
    return redirect('/home')


    
    


# @app.route('/livesearch', methods=['POST'])
# def livesearch():
#     req = request.form
#     valueData = {
#         "value": request.form['value']
#     }
#     #Run a query that SELECTS  alll users WHERE name LIKE (regex?) 
#     query = "SELECT * FROM users WHERE name LIKE  %(valueData)s%;"
#     results = connectToMySQL('moonbowpets').query_db(query, valueData)
#     #Return a jsonified version of the results
#     return jsonify(results)



