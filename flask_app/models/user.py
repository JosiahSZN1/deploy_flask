from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
mydb = 'users_schema'
# user.py
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = '''
        SELECT *
        FROM users; '''
        # results = connectToMySQL(mydb).query_db(query)
        # print(results)
        output = []
        for user_dictionary in connectToMySQL(mydb).query_db(query):
            # print(user_dictionary)
            # print(new_user)
            output.append(cls(user_dictionary))
        return output
    
    @classmethod
    def save(cls, data):
        query = '''
        INSERT INTO users(first_name, last_name, email)
        VALUES (%(first_name)s,%(last_name)s,%(email)s)
        '''
        connectToMySQL(mydb).query_db(query, data)
    
    @classmethod
    def get_one(cls,data):
        query = '''
        SELECT *
        FROM users
        WHERE id = %(id)s
        '''
        return connectToMySQL(mydb).query_db(query, data)[0]
    
    @classmethod
    def update(cls,data):
        query = '''
        UPDATE users
        SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s
        WHERE id = %(id)s
        '''
        return connectToMySQL(mydb).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = '''
        DELETE FROM users
        WHERE id = %(id)s
        '''
        return connectToMySQL(mydb).query_db(query, data)
    
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 1:
            flash("First name is required.")
            is_valid = False
        if len(data['last_name']) < 1:
            flash("Last name is required.")
            is_valid = False
        if len(data['email']) < 1:
            flash("You must provide an email.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid