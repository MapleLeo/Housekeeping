from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Housekeeper:
    db = 'housekeeping'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO housekeepers (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM housekeepers;'
        results = connectToMySQL(cls.db).query_db(query)
        housekeepers = []
        for row in results:
            housekeepers.append(cls(row))
        return housekeepers

    @classmethod
    def get_by_email(cls,data):
        query = 'SELECT * FROM housekeepers WHERE email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = 'SELECT * FROM housekeepers WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register(housekeeper):
        is_valid = True
        query = 'SELECT * FROM housekeepers WHERE email = %(email)s;'
        results = connectToMySQL(Housekeeper.db).query_db(query,housekeeper)
        if len(results) >= 1:
            flash("Email already taken.","housekeeper_register")
            is_valid = False
        if not EMAIL_REGEX.match(housekeeper['email']):
            flash("Invalid Email!!!","housekeeper_register")
            is_valid = False
        if len(housekeeper['first_name']) < 2:
            flash("First name must be at least 2 characters","housekeeper_register")
            is_valid = False
        if len(housekeeper['last_name']) < 2:
            flash("Last name must be at least 2 characters","housekeeper_register")
            is_valid = False
        if len(housekeeper['password']) < 8:
            flash("Password must be at least 8 characters","housekeeper_register")
            is_valid = False
        if housekeeper['password'] != housekeeper['confirm']:
            flash("Passwords don't match","housekeeper_register")
        return is_valid