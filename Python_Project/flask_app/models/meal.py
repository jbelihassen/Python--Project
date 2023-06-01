from flask_app.models import user
from flask import flash
from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL

class Meal:
    def __init__(self, data) :
        self.id = data['id']
        self.name = data['name']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_meals(cls):
        query = "SELECT * FROM meals ;"
        results = connectToMySQL(DATABASE).query_db(query)
        meals = []
        for row in results:
            meals.append(cls(row))
        return meals
    
    # ***   get feed_back by id  ******
 
    @classmethod
    def get_by_id_meal(cls,data):
        query = """
        SELECT * FROM meals WHERE id  = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result)< 1:
            return False
        return cls(result[0])
    


    # *** Delete Feed_Back 

    @classmethod
    def delete_meal( cls,data):
        query = """
        DELETE FROM meals WHERE id  = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
            
    @classmethod
    def create_meal(cls,data):
        query = """
        INSERT INTO meals (name,price) 
        VALUES (%(name)s, %(price)s);
        """
      
        return connectToMySQL(DATABASE).query_db(query, data)        
    @staticmethod
    def validate_meal(data):
        is_valid = True
                    
        if data['price'] == "":
            flash("price lust not be blank")
            is_valid = False        
        return is_valid
        


