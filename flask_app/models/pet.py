from flask_app.config.mysqlconnection import connectToMySQL


class Pet:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.level = data['level']
        self.description = data['description']
        self.type = data['type']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #Utility - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, username, email, password, created_at, updated_at, biography) VALUES (%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s, NOW(), NOW(), %(biography)s);"
        return connectToMySQL('moonbowpets').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('moonbowpets').query_db(query, data)