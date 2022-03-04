from flask_app import app
from flask import flash, session, render_template, request, redirect
from flask_app.models import user

@app.route('/purchase_ant')
def purchase_ant():
    data = {
        "id": session['user_id']
    }
    user.User.purchase_ant(data)
    return redirect('/shop')

@app.route('/purchase_tiger')
def purchase_tiger():
    data = {
        "id": session['user_id']
    }
    user.User.purchase_tiger(data)
    return redirect('/shop')

@app.route('/purchase_seal')
def purchase_seal():
    data = {
        "id": session['user_id']
    }
    user.User.purchase_seal(data)
    return redirect('/shop')


@app.route('/purchase_cricket')
def purchase_cricket():
    data = {
        "id": session['user_id']
    }
    user.User.purchase_cricket(data)
    return redirect('/shop')

