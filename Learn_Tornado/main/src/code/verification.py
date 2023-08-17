import tornado.web

# from ..utils.constants import Constants
# MysqlDB = Constants.Config.MysqlDB

from ...connection.mysql import MysqlDB, Sql

from firebase_admin import db

class EmailUsingSqlHandler(tornado.web.RequestHandler):
    def get(self):
        email = self.get_argument("email")
        print(f'\nChecking if the email:{email} exist ...')

        connection = Sql.get_connection(self, MysqlDB.LEARN_TORNADO1)
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM user WHERE email = %s;", [email])
        rows = cursor.rowcount
        if rows > 0:
            # email does exist
            self.set_status(200)
            self.write(f'Email:{email} verified')
        else:
            # email does not exist
            self.set_status(404)
            self.write(f'Email:{email} does not exists')
        

class EmailUsingFirebaseHandler(tornado.web.RequestHandler):
    def get(self):
        email = self.get_argument("email")
        try:
            is_email_found = False

            db_ref = db.reference('users')
            users = db_ref.get()
            for user in users:
                if user is not None:
                    is_email_found = (email == user["email"])
                if is_email_found: break

            if is_email_found:
                # email does exist
                self.set_status(200)
                self.write(f'Email:{email} verified')
            else:
                # email does not exist
                self.set_status(404)
                self.write(f'Email:{email} does not exists')

        except Exception as e:
            print(str(e))
            self.set_status(500)
            self.write("Could not fetch data from firebase")
    
    def post(self):
        try:        
            connection = Sql.get_connection(self, MysqlDB.LEARN_TORNADO1)
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, email FROM user;")

            for user in cursor.fetchall():
                db_ref = db.reference(f'users/{user[0]}')
                data = {
                        "id":user[0],
                        "name":user[1],
                        "email":user[2]
                    }
                db_ref.set(data)

            self.set_status(200)
            self.write("Data added to firebase successfully")

        except Exception as e:
            print(str(e))
            self.set_status(500)
            self.write("Could not write data in firebase")

