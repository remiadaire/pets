from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt
import re
from flask_app.models.user import User


class Pet:
    _db = "belt_exam_remi"

    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.date_found = data['date_found']
        self.count = data['count']
        self.phone_num = data['phone_num']
        self.gender = data['gender']
        self.animal_type = data['animal_type']
        self.approx_weight = data['approx_weight']
        self.age_range = data['age_range']
        self.coloring = data['coloring']
        self.demeanor = data['demeanor']
        self.unique_spots = data['unique_spots']
        self.missing_limb = data['missing_limb']
        self.noticeable_scars = data['noticeable_scars']
        self.solid_coloring = data['solid_coloring']
        self.is_fixed = data['is_fixed']
        self.multicolored = data['multicolored']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM pets;"
        results = connectToMySQL(cls._db).query_db(query)
        pets = []
        for row in results:
            pets.append(cls(row))
        return pets

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO pets (
        location, date_found, count, what_happened, user_id, phone_num, 
        gender, animal_type, approx_weight, age_range, coloring, demeanor, 
        unique_spots, missing_limb, noticeable_scars, solid_coloring, is_fixed, multicolored, 
        created_at, updated_at)
    VALUES (
        %(location)s, %(date_found)s, %(count)s, %(what_happened)s, %(user_id)s, %(phone_num)s, 
        %(gender)s, %(animal_type)s, %(approx_weight)s, %(age_range)s, %(coloring)s, %(demeanor)s, 
        %(unique_spots)s, %(missing_limb)s, %(noticeable_scars)s, %(solid_coloring)s, %(is_fixed)s, %(multicolored)s, 
        NOW(), NOW());
    """
        return connectToMySQL(cls._db).query_db(query, data)

    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM pets WHERE id = %(id)s;"
        connectToMySQL(cls._db).query_db(query, data)

    #LEFT JOINING AND PARSING DATA
    @classmethod
    def get_all_with_users(cls):
        #QUERY TO GET DATA FROM TWO TABLES
        query = """
            SELECT * from pets
            LEFT JOIN users ON pets.user_id = users.id;
        """
        results = connectToMySQL(cls._db).query_db(query)

        # print("\n\n\n\n\n\nGET ALL WITH USERS RESULTS NOT PARSED:", results)

        # #THIS ARRAY WILL HOLD ALL THE RECIPES WITH THEIR ASSOCIATED CREATOR
        list_of_all_pets_with_users = []

        #LOOP THROUGH ALL THE ROWS IN THE RESULTS
        for r in results:
            #CREATE AN RECIPE OBJECT WITH THE RECIPE DATA WE GOT FROM DB
            pet_instantace = cls(r)

            #SET UP THE USER DATA WE NEED THAT WE GOT FROM DB TO MAKE A USER OBJECT
            users_data = {
                "id" : r['users.id'],
                "first_name" : r['first_name'],
                "last_name" : r['last_name'],
                "email" : r['email'],
                "password" : r['password'],
                "created_at" : r['users.created_at'],
                "updated_at" : r['users.updated_at']
            }

            #MAKING USER OBJECT...DONT FORGET TO IMPORT THE USER CLASS(LOOK AT LINE 4)
            user_instance = User(users_data)

            #WE ARE BINDING THE USER OBJECT TO THE RECIPE ATTRIBUTE CALLED CREATOR
            pet_instantace.creator = user_instance

            #IN THE END OF THE THE ITERATION APPEND WHAT WE DID WHICH WAS HAVE A RECIPE OBJECT THAT HAS AN ATTRIBUTE THAT HOLDS THE USER OBJECT
            list_of_all_pets_with_users.append(pet_instantace)

        # #THIS PRINTS OUR AMAZING, ORGANIZED AND PARSED DATA
        # print("\n\n\n\n\n\nGET ALL WITH USERS RESULTS PARSED :", list_of_all_pets_with_users)

        # #THIS IS AN EXAMPLE OF HOW WE BREAK DOWN WHAT WE BUILT
        # print("\n\n\n\n\n\nGET ALL WITH USERS RESULTS PARSED :", list_of_all_pets_with_users[1].creator.first_name)

        #RETURN THE ARRAY THAT HOLDS ALL THE RECIPES SO WE CAN USE IT IN THE FRONT-END
        return list_of_all_pets_with_users
    

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM pets WHERE id = %(id)s;"  
        result = connectToMySQL(cls._db).query_db(query, data)
        print(f"get_by_id result: {result}") 
        if result:
            return cls(result[0])  
        return None  
    
    @classmethod
    def update(cls, data):
        query = """
        UPDATE pets
        SET location = %(location)s,
            what_happened = %(what_happened)s,
            date_found = %(date_found)s,
            count = %(count)s,
            phone_num = %(phone_num)s,
            gender = %(gender)s,
            age_range = %(age_range)s,
            coloring = %(coloring)s,
            demeanor = %(demeanor)s,
            unique_spots = %(unique_spots)s,
            approx_weight = %(approx_weight)s,
            missing_limb = %(missing_limb)s,
            noticeable_scars = %(noticeable_scars)s,
            is_fixed = %(is_fixed)s,
            multicolored = %(multicolored)s,
            solid_coloring = %(solid_coloring)s

        WHERE id = %(id)s;
        """
        # connectToMySQL(cls._db).query_db(query, data)
        return connectToMySQL(cls._db).query_db(query, data)