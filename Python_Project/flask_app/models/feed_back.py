from flask_app.config.mysqlconnection import connectToMySQL
# !!!!!!
from flask import flash
from flask_app.models import user

from flask_app import DATABASE

class Feed_back:
    def __init__(self, data) :
        self.id = data['id']
        self.user_id = data['user_id']
        self.note = data['note']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner  = user.User.get_by_id_user({'id':self.user_id})

    # *     CRUD QUERIES                       

    # ***   Create feed_backs  ******
 
    @classmethod
    def create_feed_back(cls, data):
        query = """
        INSERT INTO feed_backs (user_id, note, description) 
        VALUES (%(user_id)s, %(note)s, %(description)s);
        """
      
        return connectToMySQL(DATABASE).query_db(query, data)
    

    # ***   get_all feed_backs  ******
   
    @classmethod
    def get_feed_backs(cls):
        query = " SELECT * FROM feed_backs; "
        results = connectToMySQL(DATABASE).query_db(query)
        feed_backs = []
        for row in results:
            feed_backs.append(cls(row))
        return feed_backs
    
    # ***   get feed_back by id  ******
 
    @classmethod
    def get_by_id_feed_back(cls,data):
        query = """
        SELECT * FROM feed_backs WHERE id  = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result)< 1:
            return False
        return cls(result[0])
    


    # *** Delete Feed_Back 

    @classmethod
    def delete_feed_back(cls, data):
        query = """
        DELETE FROM feed_backs WHERE id  = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
          


    @staticmethod
    def validate_feed_back(data):
        is_valid = True
                    
        if data['description'] == "":
            flash("Description lust not be blank", "feed_back")
            is_valid = False        
        return is_valid
    