import time

def get_user_data(users, id):
   for u in users:
       if u['id'] == id:
            return u
   return None
