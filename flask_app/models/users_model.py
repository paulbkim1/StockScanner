from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile('([A-Z][a-z]*)([\\s\\\'-][A-Z][a-z]*)*')

class Users:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def check_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 letters!", "first_name")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 letters!", "last_name")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Email format is incorrect!", "email")
            is_valid = False
        else:
            email_data = {
                'email' : data['email']
            }
            potential_user = Users.check_email(email_data)
            if potential_user:
                flash("Email already taken", "email_taken")
                is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords don't match!", "password")
            is_valid = False
        return is_valid
