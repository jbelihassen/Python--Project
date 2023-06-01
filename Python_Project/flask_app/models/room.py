from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE

class Room():
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.price = data['price']
        self.images = data['images']
        self.points = data['points']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
       



    @classmethod
    def create_room(cls,data):
        query="INSERT INTO rooms (name,description,price,images,points) VALUES (%(name)s,%(description)s,%(price)s,%(images)s,%(points)s);"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_rooms(cls):
        query="SELECT * FROM rooms;"
        result=connectToMySQL(DATABASE).query_db(query)
        print(result)
        rooms=[]
        for row in result:
            rooms.append(cls(row))
        return rooms
    
    @classmethod
    def delete_room( cls,data):
        query = """
        DELETE FROM rooms WHERE id  = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_room(cls,data):
        query="SELECT * FROM rooms WHERE id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)

        if len(result)<1:
            return False
        return cls(result[0])
    
    @classmethod
    def update_room(cls,data):
        query="""UPDATE rooms SET name=%(name)s,
        description=%(description)s,price=%(price)s,images=%(images)s,points=%(points)s
        WHERE id=%(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)
    

#* SELECT LIKED ROOMS 
    @classmethod
    def liked_rooms(cls,data): #!READ
        query="""SELECT COUNT() as sumLikes FROM rooms
                JOIN likes ON rooms.id = likes.room_id
                JOIN users ON likes.user_id = users.id
                WHERE likes.room_id=%(id)s;
            """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False

        return result[0]


    # SELECT ONE LIKE
    @classmethod
    def one_like(cls,data): #!READ
        query="""SELECT * FROM rooms
                JOIN likes ON rooms.id = likes.room_id
                JOIN users ON likes.user_id = users.id
                WHERE likes.room_id=%(room_id)s AND likes.user_id=%(user_id)s;
            """
        result= connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False

        return result[0]

    #* LIKES ROOMS 
    @classmethod
    def likes_rooms(cls,data): #!CREATE
        query="""INSERT INTO likes (user_id, room_id)
                VALUES (%(user_id)s,%(room_id)s);
            """
        return connectToMySQL(DATABASE).query_db(query,data)

    #* UNLIKE ROOM
    @classmethod
    def unlikes_room(cls,data): #!DELETE
        query="DELETE FROM likes WHERE user_id=%(user_id)s AND room_id=%(room_id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    #* ALL USERS LIKES
    @classmethod
    def all_user_likes(cls,data):
        query = """
                SELECT room_id FROM likes WHERE user_id=%(user_id)s;
                """
        result= connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        if len(result)<1:
            return False

        return result[0]
    
    

    @staticmethod
    def validate_room(data):
        is_valid = True

        if len(data['name'])<1:
            flash("Name must be empty!","room")
            is_valid = False

        if len(data['description'])<1:
            flash("Description must be empty!","room")
            is_valid=False

        if len(data['price'])<1:
            flash("Price must be empty!","room")
            is_valid = False
       
      

        if len(data['points'])<1:
            flash("Points must be empty!","room")
            is_valid = False

        if len(data['price'])<1:
            flash("Price must be empty!","room")
            is_valid = False
            

        return is_valid
    



