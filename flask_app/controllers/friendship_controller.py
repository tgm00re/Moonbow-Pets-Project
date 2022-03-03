from flask_app import app
from flask import flash, session, render_template, request, redirect
from flask_app.models import user, friendship


@app.route('/friend_search')
def friend_search():
    if 'user_id' not in session:
        return redirect('/home')
    return render_template('friend-search.html')

@app.route('/search', methods=['POST'])
def search():
    if 'user_id' not in session:
        return redirect('/home')
    data = {
        "name": request.form['name']
    }
    matchingUsers = user.User.search_name(data)
    checkData = {
        "id": session['user_id']
    }
    #Friendship list to determine which actions to place in the html table
    friendshipList = friendship.Friendship.get_friendships(checkData)
    return render_template("friend-search.html", matchingUsers=matchingUsers, friendshipList=friendshipList)

@app.route('/add_friendship/<int:friend_id>')
def add_friendship(friend_id):
    if 'user_id' not in session:
        return redirect('/home')
    data = {
        "id": session['user_id'],
        "friend_id": friend_id
    }
    if friendship.Friendship.friendshipExists(data): #Friendship already exists
        return redirect('/')
    #Friendship didn't already exist:
    friendship.Friendship.save(data)
    return redirect(f'/view_profile/{data.friend_id}')

@app.route('/remove_friendship/<int:friend_id>')
def remove_friendship(friend_id):
    if 'user_id' not in session:
        return redirect('/home')
    data = {
        "id": session['user_id'],
        "friend_id": friend_id
    }
    friendship.Friendship.delete(data)
    return redirect('/friend_search')




    

