from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt
import re
from flask import flash

class User:
    _db = "belt_exam_remi"
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_registration(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        if len(form_data['email']) < 1:
            flash("Email cannot be blank", "register")
            is_valid = False
        elif not User.EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email address!", "register")
            is_valid = False
        elif User.get_by_email({"email": form_data['email']}):
            flash("Email already exists!", "register")
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if form_data['password'] != form_data['confirm_password']:
            flash("Passwords do not match", "register")
            is_valid = False
        # return 
    
        # print("Flash messages set:", dict(request.flash()))
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls._db).query_db(query, data)
    

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls._db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls._db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

