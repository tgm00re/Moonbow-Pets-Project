from flask_app.config.mysqlconnection import connectToMySQL

#NOTE: table is named 'friendship' NOT 'friendship'

class Friendship:
    def __init__(self, data):
        self.user_id = data['user_id']
        self.friend_id = data['friend_id']


    #Utility - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @classmethod
    def save(cls, data):
        query = "INSERT INTO friendship (user_id, friend_id) VALUES (%(user_id)s, %(friend_id)s);"
        return connectToMySQL('moonbowpets').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE user_id = %(id)s AND friend_id = %(friend_id)s;"
        return connectToMySQL('moonbowpets').query_db(query, data)

    @classmethod
    def get_friendships(cls, data): #get list of all friendships
        #Add user_id where data['id'] = friend_id
        queryOne = "SELECT user_id FROM friendship WHERE %(id)s = friend_id;"
        resultOne = connectToMySQL('moonbowpets').query_db(queryOne, data)
        listOne = []
        for result in resultOne:
            list.append(int(result['user_id']))
        #Add friend_id where data['id'] = user_id
        queryTwo = "SELECT friend_id FROM friendship WHERE %(id)s = user_id;"
        resultTwo = connectToMySQL('moonbowpets').query_db(queryTwo, data)
        listTwo = []
        for result in resultTwo:
            list.append(int(result['friend_id']))
        finalList = listOne + listTwo
        return finalList

    @classmethod
    def friendshipExists(cls, data): #Return a boolean  representing whether or not a friendship with the given user and friend id exists.
        queryOne = "SELECT * FROM friendship WHERE %(id)s = friend_id;"
        resultOne = connectToMySQL('moonbowpets').query_db(queryOne, data)
        if len(resultOne) >= 1:
            return True
        #Add friend_id where data['id'] = user_id
        queryTwo = "SELECT * FROM friendship WHERE %(id)s = user_id;"
        resultTwo = connectToMySQL('moonbowpets').query_db(queryTwo, data)
        if len(resultTwo) >= 1:
            return True
        return False


