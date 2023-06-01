from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask_app import DATABASE

class Admin():
    def __init__(self,data):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @classmethod
    def get_email_admin(cls,data):
        query="SELECT * FROM admins WHERE email=%(email)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)
        
        if len(result) < 1:
            return False
        return cls(result[0])
    @classmethod
    def get_by_id_admin(cls,data):
        query="SELECT * FROM admins WHERE id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result)<1:
            return False
        return cls(result[0])
    
   