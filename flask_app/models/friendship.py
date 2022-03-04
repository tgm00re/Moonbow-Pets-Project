from flask_app.config.mysqlconnection import connectToMySQL

#NOTE: table is named 'friendship' NOT 'friendship'

class Friendship:
    def __init__(self, data):
        self.user_id = data['user_id']
        self.friend_id = data['friend_id']


    #Utility - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @classmethod
    def save(cls, data):
        query = "INSERT INTO friendship (user_id, friend_id) VALUES (%(id)s, %(friend_id)s);"
        return connectToMySQL('moonbowpets').query_db(query, data)

    @classmethod
    def delete(cls, data):
        print("deleting friendship")
        query = "DELETE FROM friendship WHERE user_id = %(id)s AND friend_id = %(friend_id)s;"
        print("query two")
        queryTwo = "DELETE FROM friendship WHERE user_id = %(friend_id)s AND friend_id = %(id)s;"
        connectToMySQL('moonbowpets').query_db(query, data)
        return connectToMySQL('moonbowpets').query_db(queryTwo, data)

    @classmethod
    def get_friendships(cls, data): #get list of all friendship (ONLY IDS!)
        #Add user_id where data['id'] = friend_id
        queryOne = "SELECT user_id FROM friendship WHERE %(id)s = friend_id;"
        resultOne = connectToMySQL('moonbowpets').query_db(queryOne, data)
        listOne = []
        for result in resultOne:
            listOne.append(int(result['user_id']))
        #Add friend_id where data['id'] = user_id
        queryTwo = "SELECT friend_id FROM friendship WHERE %(id)s = user_id;"
        resultTwo = connectToMySQL('moonbowpets').query_db(queryTwo, data)
        listTwo = []
        for result in resultTwo:
            listTwo.append((result['friend_id']))
        finalList = listOne + listTwo
        print("PRINTING FINAL LIST")
        print(finalList)
        return finalList


    @classmethod
    def friendshipExists(cls, data): #Return a boolean  representing whether or not a friendship with the given user and friend id exists.
        queryOne = "SELECT * FROM friendship WHERE %(id)s = friend_id AND %(friend_id)s = user_id;"
        resultOne = connectToMySQL('moonbowpets').query_db(queryOne, data)
        if len(resultOne) >= 1:
            return True
        #Add friend_id where data['id'] = user_id
        queryTwo = "SELECT * FROM friendship WHERE %(id)s = user_id AND %(friend_id)s = friend_id;"
        resultTwo = connectToMySQL('moonbowpets').query_db(queryTwo, data)
        if len(resultTwo) >= 1:
            return True
        return False


