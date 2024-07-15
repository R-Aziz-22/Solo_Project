from flask_app.config.mysqlconnection import DB , connectToMySQL
from flask_app.models.User import User
from flask import flash

class Job:
    def __init__(self ,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.location = data['location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.user = None

    @classmethod
    def get_by_id(cls , data):
        query = "SELECT * FROM jobs JOIN users ON jobs.user_id = users.id WHERE jobs.id = %(id)s;"
        results = connectToMySQL(DB).query_db(query , data)
        if not results:
            return None
        job = cls(results[0])
        user_data = {
            'id': results[0]['users.id'],
            'email': results[0]['email'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']
        }
        job.user = User(user_data)
        return job
   
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM jobs JOIN users ON jobs.user_id = users.id;"
        results = connectToMySQL(DB).query_db(query)

        if not results:
            return []
        jobs = []
        for row in results:
            job = cls(row)
            user_data = {
                'id': row['users.id'],
                'email': row['email'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            job.user = User(user_data)
            jobs.append(job)
        return jobs
    
    @classmethod
    def create(cls , data):
        query = "INSERT INTO jobs (title , description , location, user_id) VALUES(%(title)s , %(description)s , %(location)s ,%(user_id)s);"
        return connectToMySQL(DB).query_db(query , data)
    
    @classmethod
    def update(cls , data):
        query = "UPDATE jobs SET title = %(title)s , description = %(description)s ,location = %(location)s WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query , data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM jobs WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @staticmethod
    def validate_form(data):
        is_valid = True
        if not all(list(data.values())):
            flash("All fields are required", "Register")
            is_valid = False
        
        if len(data['title'] )<= 3:
            is_valid = False
            flash("Title must be at least be 4 characters long.")
        if len(data['description'] )<= 10:
            is_valid = False
            flash("Description must be at least be 11 characters long.")
        if len(data['location'] )== 0:
            is_valid = False
            flash("Location must not be blank.")
        
        return is_valid
    
    @classmethod
    def add_to_user_jobs(cls, data):
        query = "INSERT INTO users_jobs (users_id, jobs_id) VALUES (%(users_id)s, %(jobs_id)s);"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def remove_from_user_jobs(cls, data):
        query = "DELETE FROM users_jobs WHERE users_id = %(users_id)s AND jobs_id = %(jobs_id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def get_user_jobs(cls, data):
        query = "SELECT * FROM jobs JOIN users_jobs ON jobs.id = users_jobs.jobs_id WHERE users_jobs.users_id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        if not results:
            return []
        jobs = []
        for row in results:
            job = cls(row)
            jobs.append(job)
        return jobs