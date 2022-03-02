from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.housekeeper import Housekeeper
from flask_app.models.job import Job

class Notification:
    db = 'housekeeping'
    def __init__(self,data):
        self.message = data['message']
        self.id = data['id']
    
    @classmethod
    def save(cls,data):
        query = 'INSERT INTO notifications (message, application_id, is_from_customer) VALUES (%(message)s, %(application_id)s, %(is_from_customer)s);'
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_by_application(cls, data):
        query = 'SELECT message, application_id, id, is_from_customer from notifications where application_id = %(application_id)s AND is_from_customer = %(is_from_customer)s'
        rows = connectToMySQL(cls.db).query_db(query, data)
        results = []
        for row in rows:
            results.append(cls(row))
        return results