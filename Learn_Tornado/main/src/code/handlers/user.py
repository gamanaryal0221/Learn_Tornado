from typing import Awaitable
import tornado.web
import tornado.ioloop

from ....connection.mysql import Sql, MysqlDB

from ..utils.constants import Constants
Key = Constants.Key
Url = Constants.Url

from ..services.authorization import validate_token_from_session

class UserHandler(tornado.web.RequestHandler):
    def prepare(self) -> Awaitable[None] | None:
        self.request.payload = validate_token_from_session(self)   
        return super().prepare()
    
    def get(self):

        payload = self.request.payload
        response = {
            Key.PAGE_URL: Url.USERS,
            Key.MY_FULLNAME: payload[Key.FULLNAME],
        }

        user_id = self.get_argument(Key.USER_ID, "")
        fullname = self.get_argument(Key.FULLNAME, "")
        email = self.get_argument(Key.EMAIL, "")
        number = self.get_argument(Key.NUMBER, "")

        response[Key.USER_ID] = user_id
        response[Key.FULLNAME] = fullname
        response[Key.EMAIL] = email
        response[Key.NUMBER] = number

        print(f"Search params [user_id:{user_id}, fullname:{fullname}, email:{email}, number:{number}]")

        try:

            skip_db_hit = False
            params = []
            plus_sql = ""

            if user_id:
                plus_sql = " and u.id=%s "
                try:
                    params.append(int(user_id))
                except ValueError:
                    print("Error: Invalid User id")
                    skip_db_hit = True

            if fullname and (not skip_db_hit):
                name_array = fullname.lower().split()
                print(name_array)
                size = len(name_array)
                if size==1:
                    name_array_0 = name_array[0]
                    plus_sql = plus_sql + " and (u.first_name like %s or u.middle_name like %s or u.last_name like %s) "
                    params.append(f"%{name_array_0}%")
                    params.append(f"%{name_array_0}%")
                    params.append(f"%{name_array_0}%")

                    if name_array_0=='me':
                        plus_sql = plus_sql + " or u.id=%s "
                        params.append(payload[Key.USER_ID])

                elif size==2:
                    plus_sql = plus_sql + " and u.first_name like %s and (u.middle_name like %s or u.last_name like %s) "
                    params.append(f"%{name_array[0]}%")
                    params.append(f"%{name_array[1]}%")
                    params.append(f"%{name_array[1]}%")
                elif size==3:
                    plus_sql = plus_sql + " and u.first_name like %s and u.middle_name like %s and u.last_name like %s "
                    params.append(f"%{name_array[0]}%")
                    params.append(f"%{name_array[1]}%")
                    params.append(f"%{name_array[2]}%")
                else:
                    skip_db_hit = True
            
            if email and (not skip_db_hit):
                plus_sql = plus_sql + " and ue.email like %s "
                params.append(f"%{email}%")
            
            if number and (not skip_db_hit):
                plus_sql = plus_sql + " and un.number like %s "
                params.append(f"%{number}%")


            users = []
            if not skip_db_hit:

                print (f"plus_sql:{plus_sql}")
                print (f"params:{params}")

                connection = Sql.get_connection(self, MysqlDB.LEARN_TORNADO1)
                cursor = connection.cursor()
                cursor.execute(
                    f"select u.id as {Key.USER_ID}, concat(u.first_name, ' ', coalesce(nullif(u.middle_name, ''), ''), ' ', u.last_name) as {Key.FULLNAME}, "+
                    f"concat(substring(u.first_name, 1, 1), coalesce(substring(nullif(u.middle_name, ''), 1, 1), '') ,substring(u.last_name, 1, 1)) as {Key.ALT_IMAGE_TEXT}, "+
                    f"group_concat(distinct(concat('\n',ue.email))) as {Key.EMAIL}, group_concat(distinct(concat('\n',un.number))) as {Key.NUMBER}, "+
                    f"coalesce((select up.photo_url from user_photo up where up.user_id=u.id and up.is_primary=true), case when u.gender={Constants.MALE} then '{Url.DEFAULT_MALE_PHOTO}' else '{Url.DEFAULT_FEMALE_PHOTO}' end) as {Key.PHOTO_URL} "
                    "from user u "+
                    "inner join user_email ue on ue.user_id=u.id "+
                    "inner join user_number un on un.user_id=u.id "+
                    "where 1=1 "+
                    plus_sql+
                    "group by u.id "+
                    "order by u.id desc; ", 
                    params
                )
                users = Sql.get_all_records_mapped(cursor, False)
            
            response[Key.USER_LIST] = users if users is not None else []
            self.render(Constants.HtmlFile.USERS, **response)
        
        except Exception as e:
            print(str(e))
            self.render(Url.ERROR)
