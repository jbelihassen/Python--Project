from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask_app import DATABASE

class User():
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.phone_number = data['phone_number']
        self.points = data['points']
        self.email = data['email']
        self.is_valid = data['is_valid']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.shows=[]

    #**********CRUD Queries**********
    @classmethod
    def create_user(cls,data):
        query="INSERT INTO users (first_name,last_name,phone_number,email,password) VALUES (%(first_name)s,%(last_name)s,%(phone_number)s,%(email)s,%(password)s);"
        # this query will return the id of the new user insert
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #get all users
    @classmethod
    def get_users(cls):
        query="SELECT * FROM users;"
        results= connectToMySQL(DATABASE).query_db(query)
        #organize the results
        users=[]
        for row in results:
            users.append(cls(row))
        return users
    
    #get user by id
    @classmethod
    def get_by_id_user(cls,data):
        query="SELECT * FROM users WHERE id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result)<1:
            return False
        return cls(result[0])
    

    

    @classmethod
    def get_by_email_user(cls,data):
        query="SELECT * FROM users WHERE email=%(email)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result) <1:
            return False
        return cls(result[0])
    
    
    @classmethod
    def update_user(cls,data):
        query="""UPDATE users SET first_name=%(first_name)s,
        last_name=%(last_name)s,phone_number=%(phone_number)s,email=%(email)s
        WHERE id=%(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)
       
    @classmethod
    def confirm_user(cls,id):
        query=f"""UPDATE users SET is_valid = {True} WHERE id={id};"""
        return connectToMySQL(DATABASE).query_db(query)
       
    
    @classmethod
    def delete_user(cls,data):
        query="DELETE FROM users WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
  
   
    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data['first_name'])<2:
            flash("First Name must be more than 1 characters!","register")
            is_valid = False
        if len(data['last_name'])<2:
            flash("Last Name must be more than 1 characters!","register")
            is_valid = False
        if len(data['phone_number'])<7:
            flash("phone number must be at least 8 numbers!","register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Email must be valid !","register")
            is_valid = False
        elif User.get_by_email_user({'email':data['email']}):
            flash("Email already exist !","register")
            is_valid = False
        if data['password']!=data['confirm_password']:
            flash("Passwords do not match!","register")
            is_valid = False

        return is_valid
    


    @staticmethod
    def validate_user2(data):
        is_valid = True
        if len(data['first_name'])<2:
            flash("First Name must be more than 1 characters!","register")
            is_valid = False
        if len(data['last_name'])<2:
            flash("Last Name must be more than 1 characters!","register")
            is_valid = False
        if len(data['phone_number'])<7:
            flash("phone number must be at least 8 numbers!","register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Email must be valid !","register")
            is_valid = False
        elif User.get_by_email_user({'email':data['email']}):
            flash("Email already exist !","register")
            is_valid = False
        return is_valid
