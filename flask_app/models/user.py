from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.controllers.friendship_controller import search
from flask_app.models.pet import Pet
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.biograhy = data['biography']
        self.funds = data['funds']
        self.pets = []
        self.friends = []
    

    #Utility - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @classmethod
    def save(cls, data):
        print("SAVING TO DB! :D")
        query = "INSERT INTO users (first_name, last_name, username, email, password, created_at, updated_at, biography, funds) VALUES (%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s, NOW(), NOW(), '' , 0);"
        return connectToMySQL('moonbowpets').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('moonbowpets').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('moonbowpets').query_db(query)
        users = []

        for user in results:
            users.append( cls(user) )
        return users


    @classmethod
    def get_single(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('moonbowpets').query_db(query, data)
        return cls( result[0] )

    @classmethod
    def get_all_but_self(cls, data):
        query = "SELECT * FROM users WHERE id <> %(id)s;"
        results = connectToMySQL('moonbowpets').query_db(query, data)
        users = []

        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def get_all_pets(cls, data): 
        query = "SELECT * FROM users LEFT JOIN pets ON users.id = pets.owner_id WHERE users.id = %(id)s;"
        print("Running Query")
        results = connectToMySQL('moonbowpets').query_db(query, data)
        print("Results")
        user = cls( results[0] )

        for row_from_db in results:
            pet_data = {
                "id": row_from_db['pets.id'],
                "name": row_from_db['name'],
                "level": row_from_db['level'],
                "description": row_from_db['description'],
                "type": row_from_db['type'],
                "created_at": row_from_db['pets.created_at'],
                "updated_at": row_from_db['pets.updated_at']
            }
            user.pets.append( Pet(pet_data) )
        return user

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('moonbowpets').query_db(query,data)

        if len(result) < 1:
            return False #Nobody with that email.
        return cls(result[0])


    @classmethod
    def get_all_json(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('moonbowpets').query_db(query)
        print(results)
        users = []
        for user_data in results:
            users.append( user_data )
        return users

    @classmethod
    def search_name(cls, data):
        query = "SELECT * FROM users WHERE username LIKE %(search)s;"
        searchdata = {'search': "%%" + data['name'] + "%%"}
        results = connectToMySQL('moonbowpets').query_db(query, searchdata)
        print("Printing results")
        print(results)
        users = []

        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def get_user_with_friends(cls, data): #returns single user with a list of friends
        query = "SELECT * FROM users LEFT JOIN friendship ON users.id = friendship.user_id LEFT JOIN users as users2 ON friendship.friend_id = users2.id WHERE users.id = %(id)s;"
        results = connectToMySQL('moonbowpets').query_db(query, data)
        print("Printing results")
        print(results)
        user = cls( results[0] )
        print("printing user")
        print(user)

        for row_from_db in results:
            friend_data = {
                "id": row_from_db['users2.id'],
                "first_name": row_from_db['users2.first_name'],
                "last_name": row_from_db['users2.last_name'],
                "username": row_from_db['users2.username'],
                "email": row_from_db['users2.email'],
                "password": row_from_db['users2.password'],
                "created_at": row_from_db['users2.created_at'],
                "updated_at": row_from_db['users2.updated_at'],
                "biography": row_from_db['users2.biography'],
                "funds": row_from_db["users2.funds"]
            }
            user.friends.append( cls(friend_data) )
        return user
    
    
    #purchase methods - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    @classmethod
    def purchase_tiger(cls, data):
        #Get the user and their current balance
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL('moonbowpets').query_db(query, data)
        user = cls( result[0] )
        userBalance = user.funds
        #Check if user has enough funds to pruchase the pet
        if not cls.hasEnoughFunds(userBalance, 50):
            return False #Purchase failure
        #Update the balance of the user.
        newData = {
            "newBalance": userBalance - 50,
            "id": data['id']
        }
        updateQuery = "UPDATE users SET funds=%(newBalance)s WHERE id=%(id)s;"
        updateResult = connectToMySQL('moonbowpets').query_db(updateQuery, newData)
        petData = {
            "name": 'Tony',
            "level": 1,
            "description": "They're grrrreat!",
            "type": "tiger",
            "owner_id": user.id
        }
        addPetQuery = "INSERT INTO pets (name, level, description, type, created_at, updated_at, owner_id) VALUES (%(name)s, %(level)s, %(description)s, %(type)s, NOW(), NOW(), %(owner_id)s);"
        petResult = connectToMySQL('moonbowpets').query_db(addPetQuery, petData)
        return True #Purchase success

    
    @classmethod
    def purchase_sloth(cls, data):
        #Get the user and their current balance
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL('moonbowpets').query_db(query, data)
        user = cls( result[0] )
        userBalance = user.funds
        #Check if user has enough funds to pruchase the pet
        if not cls.hasEnoughFunds(userBalance, 25):
            return False #Purchase failure
        #Update the balance of the user.
        newData = {
            "newBalance": userBalance - 25,
            "id": data['id']
        }
        updateQuery = "UPDATE users SET funds=%(newBalance)s WHERE id=%(id)s;"
        updateResult = connectToMySQL('moonbowpets').query_db(updateQuery, newData)
        petData = {
            "name": 'Sidney',
            "level": 1,
            "description": "Masters of the elements. Earth, wind, water, fi-..... Just kidding, they don't even move.",
            "type": "sloth",
            "owner_id": user.id
        }
        addPetQuery = "INSERT INTO pets (name, level, description, type, created_at, updated_at, owner_id) VALUES (%(name)s, %(level)s, %(description)s, %(type)s, NOW(), NOW(), %(owner_id)s);"
        petResult = connectToMySQL('moonbowpets').query_db(addPetQuery, petData)
        return True #Purchase success

    @classmethod
    def purchase_seal(cls, data):
        #Get the user and their current balance
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL('moonbowpets').query_db(query, data)
        user = cls( result[0] )
        userBalance = user.funds
        #Check if user has enough funds to pruchase the pet
        if not cls.hasEnoughFunds(userBalance, 25):
            return False #Purchase failure
        #Update the balance of the user.
        newData = {
            "newBalance": userBalance - 25,
            "id": data['id']
        }
        updateQuery = "UPDATE users SET funds=%(newBalance)s WHERE id=%(id)s;"
        updateResult = connectToMySQL('moonbowpets').query_db(updateQuery, newData)
        petData = {
            "name": 'Saul',
            "level": 1,
            "description": "Way too cute to attack you, right? ....right???",
            "type": "seal",
            "owner_id": user.id
        }
        addPetQuery = "INSERT INTO pets (name, level, description, type, created_at, updated_at, owner_id) VALUES (%(name)s, %(level)s, %(description)s, %(type)s, NOW(), NOW(), %(owner_id)s);"
        petResult = connectToMySQL('moonbowpets').query_db(addPetQuery, petData)
        return True #Purchase success

    @classmethod
    def purchase_scorpion(cls, data):
        #Get the user and their current balance
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL('moonbowpets').query_db(query, data)
        user = cls( result[0] )
        userBalance = user.funds
        #Check if user has enough funds to pruchase the pet
        if not cls.hasEnoughFunds(userBalance, 50):
            return False #Purchase failure
        #Update the balance of the user.
        newData = {
            "newBalance": userBalance - 50,
            "id": data['id']
        }
        updateQuery = "UPDATE users SET funds=%(newBalance)s WHERE id=%(id)s;"
        updateResult = connectToMySQL('moonbowpets').query_db(updateQuery, newData)
        petData = {
            "name": 'Sally',
            "level": 1,
            "description": "A kunai-spear wielding ninja on a quest to avenge the deaths of his famil- No? Not that one ... these are just little creatures that kill things with a spiked tail for no reason",
            "type": "scorpion",
            "owner_id": user.id
        }
        addPetQuery = "INSERT INTO pets (name, level, description, type, created_at, updated_at, owner_id) VALUES (%(name)s, %(level)s, %(description)s, %(type)s, NOW(), NOW(), %(owner_id)s);"
        petResult = connectToMySQL('moonbowpets').query_db(addPetQuery, petData)
        return True #Purchase success

    @classmethod
    def purchase_cricket(cls, data):
        #Get the user and their current balance
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL('moonbowpets').query_db(query, data)
        user = cls( result[0] )
        userBalance = user.funds
        #Check if user has enough funds to pruchase the pet
        if not cls.hasEnoughFunds(userBalance, 50):
            return False #Purchase failure
        #Update the balance of the user.
        newData = {
            "newBalance": userBalance - 50,
            "id": data['id']
        }
        updateQuery = "UPDATE users SET funds=%(newBalance)s WHERE id=%(id)s;"
        updateResult = connectToMySQL('moonbowpets').query_db(updateQuery, newData)
        petData = {
            "name": 'Carl',
            "level": 1,
            "description": "A little fella that loves to keep you up at night!",
            "type": "cricket",
            "owner_id": user.id
        }
        addPetQuery = "INSERT INTO pets (name, level, description, type, created_at, updated_at, owner_id) VALUES (%(name)s, %(level)s, %(description)s, %(type)s, NOW(), NOW(), %(owner_id)s);"
        petResult = connectToMySQL('moonbowpets').query_db(addPetQuery, petData)
        return True #Purchase success

    @classmethod
    def purchase_cat(cls, data):
        #Get the user and their current balance
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL('moonbowpets').query_db(query, data)
        user = cls( result[0] )
        userBalance = user.funds
        #Check if user has enough funds to pruchase the pet
        if not cls.hasEnoughFunds(userBalance, 75):
            return False #Purchase failure
        #Update the balance of the user.
        newData = {
            "newBalance": userBalance - 75,
            "id": data['id']
        }
        updateQuery = "UPDATE users SET funds=%(newBalance)s WHERE id=%(id)s;"
        updateResult = connectToMySQL('moonbowpets').query_db(updateQuery, newData)
        petData = {
            "name": 'Arthur',
            "level": 1,
            "description": "Adorable little creatures that love to cuddle! They just happen to have razor sharp claws that can slash out your eyes :)",
            "type": "cat",
            "owner_id": user.id
        }
        addPetQuery = "INSERT INTO pets (name, level, description, type, created_at, updated_at, owner_id) VALUES (%(name)s, %(level)s, %(description)s, %(type)s, NOW(), NOW(), %(owner_id)s);"
        petResult = connectToMySQL('moonbowpets').query_db(addPetQuery, petData)
        return True #Purchase success

    @classmethod
    def purchase_ant(cls, data):
        #Get the user and their current balance
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL('moonbowpets').query_db(query, data)
        user = cls( result[0] )
        userBalance = user.funds
        #Check if user has enough funds to pruchase the pet
        if not cls.hasEnoughFunds(userBalance, 50):
            return False #Purchase failure
        #Update the balance of the user.
        newData = {
            "newBalance": userBalance - 50,
            "id": data['id']
        }
        updateQuery = "UPDATE users SET funds=%(newBalance)s WHERE id=%(id)s;"
        updateResult = connectToMySQL('moonbowpets').query_db(updateQuery, newData)
        petData = {
            "name": 'Alexander',
            "level": 1,
            "description": "The ant is a fairly social creature that greatly enjoys runining your picnics!",
            "type": "cricket",
            "owner_id": user.id
        }
        addPetQuery = "INSERT INTO pets (name, level, description, type, created_at, updated_at, owner_id) VALUES (%(name)s, %(level)s, %(description)s, %(type)s, NOW(), NOW(), %(owner_id)s);"
        petResult = connectToMySQL('moonbowpets').query_db(addPetQuery, petData)
        return True #Purchase success


    @classmethod
    def add_funds(cls, data): #takes in a data dictionary of both the newbalance and the user's id
        query = "UPDATE users SET funds=%(newBalance)s WHERE id = %(id)s;"
        return connectToMySQL('moonbowpets').query_db(query, data)
    
        

    
    


    #Staticmethods - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2 or len(user['last_name']) < 2:
            flash("First and last name must be two or more characters.",'register')
            is_valid = False
        if len(user['username']) < 4:
            flash("Username must be 4 or more characters", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address", 'register')
            is_valid = False
        if len(user['password']) < 5:
            flash("Password must be 5 or more characters", 'register')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords must match", 'register')
            is_valid = False
        return is_valid


    
    @staticmethod
    def hasEnoughFunds(balance, price):
        if balance >= price:
            return True
        return False
        