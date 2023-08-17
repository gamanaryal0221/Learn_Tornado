from typing import Awaitable
import tornado.web
import tornado.ioloop

from ...code.utils.constants import Constants
Key = Constants.Key

from ..services.authorization import validate_token_from_session, get_cookie

class HomeHandler(tornado.web.RequestHandler):
    def prepare(self) -> Awaitable[None] | None:
        self.request.payload = validate_token_from_session(self)   
        return super().prepare()


    def get(self):
        payload = self.request.payload
        print(f"payload:{payload}")
        response = {
            Key.MY_FULLNAME: payload[Key.FULLNAME],
        }
        self.render(Constants.HtmlFile.HOME, **response)


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        print(f'Logout successful for user[id:{get_cookie(self, Key.USER_ID)}, email:{get_cookie(self, Key.EMAIL)}]')
        self.redirect(Constants.Url.HOME)


                    # cursor = connection.cursor()
                    # cursor.execute(
                    #     "SELECT cm.chat_id, concat(u1.first_name, ' ', u1.last_name), concat(u2.first_name, ' ', u2.last_name) from chat_member cm "+
                    #     "inner join user u on u.id=cm.user2_id "+
                    #     "where (cm.user1_id=%s and cm.user_joined_at is not null) or (cm.user2_id=%s and cm.another_user_joined_at is not null) ",
                    #     [session_user_id, session_user_id]
                    # )
                    # chats = cursor.fetchall()
                    # print(chats)