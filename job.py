from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from base64 import b64encode
from flask_app.models.customer import Customer

class Job:
    db = 'housekeeping'
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.date = data['date']
        self.time = data['time']
        self.pay = data['pay']
        self.description = data['description']
        self.customer_id = data['customer_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        if('customers.id' in data):
            self.customer = Customer(dict(
                data,
                id=data['customer_id'],
                created_at=data['customers.created_at'],
                updated_at=data['customers.updated_at'],
            ))

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO jobs (title, date, time, pay, description, customer_id) VALUES (%(title)s, %(date)s, %(time)s, %(pay)s, %(description)s, %(customer_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_customer(cls, data):
        query = 'SELECT * FROM jobs WHERE customer_id = %(customer_id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        all_jobs = []
        for row in results:
            all_jobs.append(cls(row))
        return all_jobs

    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM jobs WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_all_available_with_customer(cls):
        query = 'SELECT * FROM jobs JOIN customers on customers.id = jobs.customer_id WHERE (SELECT count(*) from applications where applications.job_id = jobs.id AND applications.status = "APPROVED") = 0;'
        results = connectToMySQL(cls.db).query_db(query)
        all_jobs = []
        for row in results:
            all_jobs.append(cls(row))
        return all_jobs

    @classmethod
    def job_destroy(cls,data):
        query = 'DELETE FROM jobs WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_by_housekeeper(cls, housekeeper_id):
        query = 'SELECT * FROM jobs JOIN applications on applications.job_id = jobs.id where applications.status = "APPROVED" and applications.housekeeper_id = %(housekeeper_id)s;'
        results = connectToMySQL(cls.db).query_db(query, { 'housekeeper_id': housekeeper_id })
        all_jobs = []
        for row in results:
            all_jobs.append(cls(row))
        return all_jobs

    @staticmethod
    def validate_job(job):
        is_valid = True
        if len(job['title']) == 0:
            is_valid = False
            flash("Title is required","job")
        if len(job['time']) < 0:
            is_valid = False
            flash("Job time is required","job") 
        return is_valid