from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime
from flask_app.models import user
from flask_app.models import room
from flask_app.models import meal
import re	  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask_app import DATABASE

class Reservation():
    def __init__(self,data):
        self.id = data['id']
        self.meal_id = data['meal_id']
        self.user_id = data['user_id']
        self.room_id = data['room_id']        
        self.how_many_person = data['how_many_person']
        self.check_in = data ['check_in']
        self.check_out = data ['check_out']
        self.is_confirmed = data['is_confirmed']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = user.User.get_by_id_user({'id':self.user_id})
        self.room= room.Room.get_room({'id':self.room_id})
        self.meal= meal.Meal.get_by_id_meal({'id':self.meal_id})

    #**********CRUD Queries**********

    @classmethod
    def confirm_reservation(cls,id):
        query=f"""UPDATE reservations SET is_confirmed = {True} WHERE id={id};"""
        return connectToMySQL(DATABASE).query_db(query)
       

    
    @classmethod
    def create_reservation(cls,data):
        print(data,"*"*23)
        query="""
                    INSERT INTO reservations (user_id,room_id,how_many_person,check_in,check_out,meal_id) 
                    VALUES (%(user_id)s,%(room_id)s,%(how_many_person)s,%(check_in)s,%(check_out)s,%(meal_id)s);
            """
        # this query will return the id of the new user insert
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #get all reservations

    @classmethod
    def get_all_reservations(cls):
        query="SELECT * FROM reservations;"
        results= connectToMySQL(DATABASE).query_db(query)
        #organize the results
        reservations=[]
        for row in results:
            reservations.append(cls(row))
        return reservations
    
    #get reservation by id

    @classmethod
    def get_by_id_reservation(cls,data):
        query="SELECT * FROM reservations WHERE id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result)<1:
            return False
        return cls(result[0])
    

    @classmethod
    def get_by_email_reservation(cls,data):
        query="SELECT * FROM reservations WHERE email=%(email)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result) <1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_confirmed_reservation(cls, data):
        query = """ SELECT * FROM  reservations WHERE room_id = %(room_id)s and check_out > NOW() and is_confirmed = 1 ;"""   
        results = connectToMySQL(DATABASE).query_db(query,data)
        confirmed_reservation = []
        if len(results) == 0:
            return False
        for row in results:
            confirmed_reservation.append(cls(row))
        return confirmed_reservation

    @classmethod
    def delete_reservation(cls,data):
        query="DELETE FROM reservations WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @staticmethod
    def validate_reservation(data):
        print(data,"="*23)
        is_valid = True
        if datetime.strptime(data['check_in'],"%Y-%m-%d").date() < datetime.now().date():
            flash("check in choose a good date!","reservation")
            is_valid = False
        if datetime.strptime(data['check_out'],"%Y-%m-%d").date() < datetime.now().date():
            flash("check out choose a good date!!","reservation")
            is_valid = False
        if datetime.strptime(data['check_out'],"%Y-%m-%d").date() < datetime.strptime(data['check_in'],"%Y-%m-%d").date():
            flash("check in date most be before than the check out date !","reservation")
            is_valid = False
        return is_valid
    
   