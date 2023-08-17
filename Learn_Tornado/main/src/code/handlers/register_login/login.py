import tornado.web
import tornado.ioloop

from .....connection.mysql import MysqlDB, Sql
from ...utils.constants import Constants
login_page = Constants.HtmlFile.LOGIN
Key = Constants.Key

from ...services.authorization import generate_token_and_save_in_cookie, Password
from ...utils.helper import is_valid_email

response = {
    Key.EMAIL_OR_NUMBER:"",
    Key.PASSWORD: "",
    Key.ERROR_MSG: ""
}

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        response[Key.EMAIL_OR_NUMBER] = ""
        response[Key.PASSWORD] = ""
        response[Key.ERROR_MSG] = ""
        self.render(login_page, **response)

    def post(self):
        email_or_number = self.get_argument(Key.EMAIL_OR_NUMBER, "")
        password = self.get_argument(Key.PASSWORD, "")

        response[Key.EMAIL_OR_NUMBER] = email_or_number
        response[Key.PASSWORD] = password

        if email_or_number and password:
            print(f'\nVerifying the credentials ...')

            try:

                is_email = is_valid_email(email_or_number)
                print(f"{email_or_number} is email?\n >>{is_email}")
                plus_sql = ""
                if is_email:
                    plus_sql = " ue.email=%s "
                else:
                    plus_sql = " un.number=%s "

                connection = Sql.get_connection(self, MysqlDB.LEARN_TORNADO1)
                cursor = connection.cursor()
                cursor.execute(
                    f"select u.id as {Key.USER_ID}, ue.email as {Key.EMAIL}, un.number as {Key.NUMBER}, "+
                    f"u.first_name as {Key.FIRST_NAME}, u.middle_name as {Key.MIDDLE_NAME}, u.last_name as {Key.LAST_NAME}, "+
                    f"u.salt_value as {Key.SALT_VALUE}, u.password as {Key.HASHED_PASSWORD} "
                    "from user u "+
                    "inner join user_email ue on ue.user_id=u.id "+
                    "inner join user_number un on un.user_id=u.id "+
                    "where ue.is_primary=true and un.is_primary=true "+
                    "and " + plus_sql, 
                    [email_or_number]
                )
                user = Sql.get_all_records_mapped(cursor)
                
                if user:
                    
                    if Password.is_valid(user, password):
                        print(f'Login successful for user[id:{user[Key.USER_ID]}]')                    
                        try:
                            generate_token_and_save_in_cookie(self,user)
                            self.redirect(Constants.Url.HOME)
                        except Exception as e:
                            print(str(e))
                            print('Error occured in token generation -> Redirecting to login page')
                            response[Key.ERROR_MSG] = "Something went wrong. Please try again later"
                            self.render(login_page,**response)
                    else:
                        response[Key.ERROR_MSG] = f"{'Email' if is_email else 'Number'} and password combination is not determined to be authentic."
                        self.render(login_page,**response)
                else:
                    response[Key.ERROR_MSG] = "Login failed. Please check your credentials and try again."
                    self.render(login_page,**response)
            
            except Exception as e:
                print(str(e))
                response[Key.ERROR_MSG] = "Something went wrong. Please try again later"
                self.render(login_page,**response)

        else:
            response[Key.ERROR_MSG] = "Email and password are mandatory"
            self.render(login_page,**response)
