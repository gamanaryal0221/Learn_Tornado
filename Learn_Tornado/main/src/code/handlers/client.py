from typing import Awaitable
import tornado.web
import tornado.ioloop

from ....connection.mysql import Sql, MysqlDB

from ..utils.constants import Constants
Key = Constants.Key
Url = Constants.Url

from ..services.authorization import validate_token_from_session


class ClientListHandler(tornado.web.RequestHandler):
    def prepare(self) -> Awaitable[None] | None:
        self.request.payload = validate_token_from_session(self)   
        return super().prepare()
    
    def get(self):
        payload = self.request.payload
        response = {
            Key.PAGE_URL: Url.CLIENTS,
            Key.MY_FULLNAME: payload[Key.FULLNAME],
        }

        client_id = self.get_argument(Key.CLIENT_ID, "")
        client_name = self.get_argument(Key.NAME, "")
        email = self.get_argument(Key.EMAIL, "")
        number = self.get_argument(Key.NUMBER, "")

        response[Key.CLIENT_ID] = client_id
        response[Key.NAME] = client_name
        response[Key.EMAIL] = email
        response[Key.NUMBER] = number

        print(f"Search params [client_id:{client_id}, client_name:{client_name}, email:{email}, number:{number}]")

        try:

            skip_db_hit = False
            params = []
            plus_sql = ""

            if client_id:
                plus_sql = " and c.id=%s "
                try:
                    params.append(int(client_id))
                except ValueError:
                    print("Error: Invalid Client id")
                    skip_db_hit = True

            if client_name and (not skip_db_hit):
                plus_sql = plus_sql + " and ( c.name like %s or c.display_name like %s ) "
                params.append(f"%{client_name}%")
                params.append(f"%{client_name}%")
            
            if email and (not skip_db_hit):
                plus_sql = plus_sql + " and ce.email like %s "
                params.append(f"%{email}%")
            
            if number and (not skip_db_hit):
                plus_sql = plus_sql + " and cn.number like %s "
                params.append(f"%{number}%")


            clients = []
            if not skip_db_hit:

                print (f"plus_sql:{plus_sql}")
                print (f"params:{params}")

                connection = Sql.get_connection(self, MysqlDB.LEARN_TORNADO1)
                cursor = connection.cursor()
                cursor.execute(
                    f"select c.id as {Key.CLIENT_ID}, c.name as {Key.NAME}, c.display_name as {Key.DISPLAY_NAME}, "+
                    f"group_concat(distinct(concat('\n',ce.email))) as {Key.EMAIL}, group_concat(distinct(concat('\n',cn.number))) as {Key.NUMBER} "+
                    "from client c "+
                    "inner join client_email ce on ce.client_id=c.id "+
                    "inner join client_number cn on cn.client_id=c.id "+
                    "where 1=1 "+
                    plus_sql+
                    "group by c.id "+
                    "order by c.id desc; ", 
                    params
                )
                clients = Sql.get_all_records_mapped(cursor, False)

            print(f"clients: {clients}")
            
            response[Key.CLIENT_LIST] = clients if clients is not None else []
            self.render(Constants.HtmlFile.CLIENTS, **response)
        
        except Exception as e:
            print(str(e))
            self.render(Url.ERROR)