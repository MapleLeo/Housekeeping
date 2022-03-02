from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.housekeeper import Housekeeper
from flask_app.models.job import Job

class Application:
    db = 'housekeeping'
    def __init__(self,data):
        self.id = data['id']
        self.status = data['status']
        self.resume = data['resume']
        self.housekeeper_id = data['housekeeper_id']
        self.job_id = data['job_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.notification_count = data.get('notification_count')
        if('jobs.id' in data):
            self.job = Job(dict(
                data,
                id=data['job_id'],
                created_at=data['jobs.created_at'],
                updated_at=data['jobs.updated_at']))
        if('housekeepers.id' in data):
            self.housekeeper = Housekeeper(dict(
                data,
                id=data['housekeeper_id'],
                created_at=data['housekeepers.created_at'],
                updated_at=data['housekeepers.updated_at']))

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO applications (status, resume, housekeeper_id, job_id) VALUES (%(status)s, %(resume)s, %(housekeeper_id)s, %(job_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_for_housekeeper_account(cls, housekeeper_id):
        query = 'SELECT'\
            '*, '\
            '(select count(*) from notifications where notifications.application_id = applications.id AND notifications.is_from_customer = 0) as notification_count '\
            'FROM applications '\
            'LEFT JOIN jobs on applications.job_id = jobs.id '\
            'JOIN customers on customers.id = jobs.customer_id '\
            'where applications.housekeeper_id = %(housekeeper_id)s;'
        results = connectToMySQL(cls.db).query_db(query, {'housekeeper_id': housekeeper_id})
        print(results)
        applications = []
        for row in results:
            applications.append(cls(row))
        return applications
    
    @classmethod
    def get_by_customer_with_job_and_housekeeper(cls, customer_id):
        query = 'SELECT *, '\
            '(select count(*) from notifications where notifications.application_id = applications.id AND notifications.is_from_customer = 1) as notification_count, '\
            'housekeepers.id as `housekeepers.id` '\
            'FROM applications '\
            'LEFT JOIN jobs on applications.job_id = jobs.id '\
            'LEFT JOIN housekeepers on applications.housekeeper_id = housekeepers.id '\
            'where jobs.customer_id = %(customer_id)s AND '\
            'applications.status = "PENDING"'
        
        results = connectToMySQL(cls.db).query_db(query, {'customer_id': customer_id})
        applications = []
        for row in results:
            applications.append(cls(row))
        return applications

    @classmethod
    def set_status(cls, id, status):
        query = 'update applications set `status` = %(status)s where id=%(id)s;'
        return connectToMySQL(cls.db).query_db(query, {'id': id, 'status': status})
