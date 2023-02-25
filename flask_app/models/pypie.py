from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
db = "pypies"

class Pie:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.filling = data['filling']
        self.crust = data['crust']
        self.votes = data['votes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM pies ORDER BY votes DESC;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(db).query_db(query)
        # Create an empty list to append our instances of friends
        pies = []
        # Iterate over the db results and create instances of friends with cls.
        for pie in results:
            pies.append( cls(pie) )
        return pies
    @classmethod
    def save(cls, data):
        query = "INSERT INTO pies (name, filling, crust, user_id) VALUES (%(name)s, %(filling)s, %(crust)s, %(user_id)s);"
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM pies WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])
    @classmethod
    def update(cls,data):
        query = "UPDATE pies SET name=%(name)s, filling=%(filling)s, crust=%(crust)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)
    @classmethod
    def update_votes(cls,data):
        query = "UPDATE pies SET votes=votes + 1 WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)
    @classmethod
    def dec_votes(cls,data):
        query = "UPDATE pies SET votes=votes - 1 WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM pies WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)
    @staticmethod
    def validate_pie(pie):
        is_valid = True # we assume this is true
        if len(pie['name']) < 2:
            flash("Name must be at least 2 characters.")
            is_valid = False
        if len(pie['filling']) < 2:
            flash("Filling must be at least 2 characters.")
            is_valid = False
        if len(pie['crust']) < 2:
            flash("Instructions must be at least 2 characters")
            is_valid = False
        return is_valid
    @staticmethod
    def check_vote_status(data):
        query = "SELECT * FROM vote_status;"
        results = connectToMySQL(db).query_db(query)
        for row in results:
            if row['user_id'] == data['user_id'] and row['pie_id'] == data['pie_id']:
                return False
        return True
    @staticmethod
    def add_vote_status(data):
        query = "INSERT INTO vote_status (user_id, pie_id) VALUES (%(user_id)s, %(pie_id)s);"
        return connectToMySQL(db).query_db(query, data)
    @staticmethod
    def destroy_vote_status(data):
        query = "DELETE FROM vote_status WHERE user_id = %(user_id)s AND pie_id = %(pie_id)s;"
        return connectToMySQL(db).query_db(query,data)

    