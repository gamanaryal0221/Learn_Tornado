import tornado.web
import tornado.ioloop

from .....connection.mysql import MysqlDB, Sql
from ...utils.constants import Constants
registration_page = Constants.HtmlFile.REGISTRATION
Key = Constants.Key

from ....code.services.authorization import Password

response = {
    Key.FIRST_NAME:"",
    Key.MIDDLE_NAME: "",
    Key.LAST_NAME: "",
    Key.EMAIL:"",
    Key.NUMBER:"",
    Key.PASSWORD: "",
    Key.ERROR_MSG: ""
}

class RegistrationHandler(tornado.web.RequestHandler):
    def get(self):
        response[Key.FIRST_NAME] = ""
        response[Key.MIDDLE_NAME] = ""
        response[Key.LAST_NAME] = ""
        response[Key.EMAIL] = ""
        response[Key.NUMBER] = ""
        response[Key.PASSWORD] = ""
        response[Key.ERROR_MSG] = ""
        self.render(registration_page, **response)

    def post(self):
        first_name = self.get_argument(Key.FIRST_NAME, "")
        middle_name = self.get_argument(Key.MIDDLE_NAME, "")
        last_name = self.get_argument(Key.LAST_NAME, "")
        gender = self.get_argument(Key.GENDER, "")
        email = self.get_argument(Key.EMAIL, "")
        number = self.get_argument(Key.NUMBER, "")
        password = self.get_argument(Key.PASSWORD, "")

        response[Key.FIRST_NAME] = first_name
        response[Key.MIDDLE_NAME] = middle_name
        response[Key.LAST_NAME] = last_name
        response[Key.EMAIL] = email
        response[Key.NUMBER] = number
        response[Key.PASSWORD] = password
        
        if first_name and last_name and gender and email and number and password:

            try:

                if len(number) == 10:
                    print(f'\nChecking if the number:{number} already exist ...')

                    connection = Sql.get_connection(self, MysqlDB.LEARN_TORNADO1)
                    cursor = connection.cursor()
                    cursor.execute("SELECT number FROM user_number WHERE number=%s;", [number])

                    if cursor.rowcount > 0:
                        response[Key.ERROR_MSG] = f"Number:{number} is already taken."
                        self.render(registration_page,**response)
                    else:

                        print(f'\nChecking if the email:{email} already exist ...')
                        cursor = connection.cursor()
                        cursor.execute("SELECT email FROM user_email WHERE email=%s;", [email])

                        if cursor.rowcount > 0:
                            response[Key.ERROR_MSG] = f"Email:{email} is already taken."
                            self.render(registration_page,**response)
                        else:
                            print("Creating user ...")
                            password_detail = Password.encrypt(password)

                            cursor = connection.cursor()
                            cursor.execute(
                                "INSERT INTO user (first_name, middle_name, last_name, gender, salt_value, password) "+
                                "VALUES (%s, %s, %s, %s, %s, %s);",
                                [first_name.capitalize(), middle_name.capitalize(), last_name.capitalize(), int(gender), password_detail[Key.SALT_VALUE], password_detail[Key.HASHED_PASSWORD]]
                            )

                            user_id = cursor.lastrowid

                            if user_id is not None:
                                print(f'Adding primary email:{email} of user[id:{user_id}] ...')
                                cursor = connection.cursor()
                                cursor.execute(
                                    "INSERT INTO user_email (user_id, email, is_primary) VALUES (%s, %s, %s);",
                                    [user_id, email.lower(), True]
                                )

                                if cursor.lastrowid is not None:      
                                    print(f'Adding primary number:{number} of user[id:{user_id}] ...')
                                    cursor = connection.cursor()
                                    cursor.execute(
                                        "INSERT INTO user_number (user_id, number, is_primary) VALUES (%s, %s, %s);",
                                        [user_id, number, True]
                                    )

                                    if cursor.lastrowid is not None:                          
                                        print(f'User[id:{user_id}] successfully created')
                                        self.redirect(Constants.Url.LOGIN)
                                    else:
                                        raise RuntimeError(f'Failed to insert primary number:{number} of user[id:{user_id}]')
                                    
                                else:
                                    raise RuntimeError(f'Failed to insert primary email:{email} of user[id:{user_id}]')

                            else:
                                raise RuntimeError("Failed to insert user record")
                        
                else:
                    response[Key.ERROR_MSG] = f"Please provide your valid number."
                    self.render(registration_page,**response)

            except Exception as e:
                print(str(e))
                response[Key.ERROR_MSG] = "Something went wrong. Please try again later."
                self.render(registration_page,**response)

        else:
            response[Key.ERROR_MSG] = "All fields are mandatory."
            self.render(registration_page,**response)