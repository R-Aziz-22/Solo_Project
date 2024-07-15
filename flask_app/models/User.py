from flask_app.config.mysqlconnection import DB , connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register(cls , data):
        encrypted_password = bcrypt.generate_password_hash(data['password'])
        data = dict(data)
        data['password'] = encrypted_password

        query = "INSERT INTO users (first_name , last_name , email , password) VALUES(%(first_name)s , %(last_name)s , %(email)s , %(password)s);"
        return connectToMySQL(DB).query_db(query , data)
    
    @classmethod
    def get_by_id(cls , data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query , data)

        if results:
            return cls(results[0])
        return None
    
    @classmethod
    def get_by_email(cls , data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DB).query_db(query , data)

        if results:
            return cls(results[0])
        return None
    
    @staticmethod
    def validate_register(data):
        is_valid = True
        user_in_db = User.get_by_email(data)

        if not all(list(data.values())):
            flash("All fields are required", "Register")
            is_valid = False

        if len(data['first_name'] )< 2:
            is_valid = False
            flash("First name must be at least be 2 characters long.")
        if len(data['last_name'] )< 2:
            is_valid = False
            flash("Last name must be at least be 2 characters long.")
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Invalid Email.")
        if user_in_db:
            is_valid = False
            flash("This email already exists in the database.")
        if len(data['password']) < 8:
            is_valid = False
            flash("Password must at least be 8 characters long.")

        if data['password'] != data['confirm_pw']:
            is_valid = False
            flash("Passwords must match.")

        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        user_in_db = User.get_by_email(data)

        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Invalid Email.")
        if not user_in_db:
            is_valid = False
            flash("Email doesn't exist in our database.")
        elif not bcrypt.check_password_hash(user_in_db.password , data['password']):
            is_valid = False
            flash("Incorrect Password")

        return is_valid