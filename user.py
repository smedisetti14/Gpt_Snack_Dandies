from flask_login import UserMixin
from firebase_admin import auth
import json

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id, data_handler):
        #print(data_handler.get_user_schema(user_id))
        return data_handler.get_user_schema(user_id)
    
    @staticmethod
    def create(user_id, name, email, picture, data_handler):
        user = User(user_id,name,email,picture)
        data_handler.insert_or_update_user_schema(user)

    def toJson(self):
        # generate json from self object
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)
    
    

         

