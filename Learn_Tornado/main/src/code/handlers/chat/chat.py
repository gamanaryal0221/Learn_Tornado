from typing import Awaitable, Optional
import tornado.web
import tornado.ioloop
import tornado.websocket

from ...utils.constants import Constants
Key = Constants.Key
Url = Constants.Url
ChatHtmlFile = Constants.HtmlFile.CHAT

from .....connection.mysql import MysqlDB, Sql

from ...services.authorization import validate_token_from_session

# List to store connected clients
connected_clients = []

class ChatListHandler(tornado.web.RequestHandler):
    def get(self):
        print("going here")
        self.redirect(ChatHtmlFile)


class ChatHandler(tornado.web.RequestHandler):
    def prepare(self) -> Awaitable[None] | None:
        self.request.payload = validate_token_from_session(self)
        return super().prepare()
    
    def get(self):
        payload= self.request.payload
        session_user_id = payload[Key.USER_ID]
        chat_id = self.get_argument(Key.CHAT_ID,'')
        user_id = self.get_argument(Key.USER_ID,'')

        payload = self.request.payload
        response = {
            Key.MY_FULLNAME: payload[Key.FULLNAME],
        }

        if chat_id:

            response[Key.CHAT_ID] = chat_id
        
            connection = Sql.get_connection(self, MysqlDB.LEARN_TORNADO1)
            cursor = connection.cursor()
            cursor.execute(f"select is_group_chat as {Key.IS_GROUP_CHAT}, name as {Key.CHAT_NAME}, SUBSTRING(name, 1, 1) as {Key.ALT_IMAGE_TEXT} from chat where id=%s",[chat_id])
            chat_detail = Sql.get_all_records_mapped(cursor)
            if chat_detail:

                response[Key.IS_GROUP_CHAT] = chat_detail[Key.IS_GROUP_CHAT]
                response[Key.CHAT_NAME] = chat_detail[Key.CHAT_NAME]
                response[Key.ALT_IMAGE_TEXT] = chat_detail[Key.ALT_IMAGE_TEXT]

                if response[Key.IS_GROUP_CHAT]:

                    if not response[Key.CHAT_NAME]:
                        cursor = connection.cursor()
                        cursor.execute(
                            f"select (case when (c.name is null or c.name='') then group_concat(u.first_name) else c.name) as {Key.CHAT_NAME}, SUBSTRING(group_concat(u.first_name), 1, 1) as {Key.ALT_IMAGE_TEXT} from chat c "+
                            "inner join group_chat_member gcm on gcm.chat_id=c.id "+
                            "inner join user u on u.id=gcm.user_id "+
                            "WHERE c.id=%s and cm.user_id<>%s "+
                            "group by c.id;", 
                            [chat_id, session_user_id]
                        )
                        chat_names = Sql.get_all_records_mapped(cursor)
                        response[Key.CHAT_NAME] = chat_names[Key.CHAT_NAME]
                        response[Key.ALT_IMAGE_TEXT] = chat_names[Key.ALT_IMAGE_TEXT]

                    cursor = connection.cursor()
                    cursor.execute(
                        f"select concat(u.first_name, ' ', u.last_name) as {Key.FULLNAME}, gcm.is_admin as {Key.IS_ADMIN}, gcm.joined_at as {Key.JOINED_AT}, concat(ab.first_name, ' ', ab.last_name) as {Key.ADDED_BY} "+
                        "from group_chat_member gcm "+
                        "inner join user u on gcm.user_id=u.id "+
                        "inner join user ab on gcm.added_by=ab.id;"
                    )
                    response[Key.MEMBERS] = Sql.get_all_records_mapped(cursor)

                    print(response)
                    return response
                else:

                    if not response[Key.CHAT_NAME]:
                        cursor = connection.cursor()
                        cursor.execute(
                            f"select group_concat(first_name, ' ', last_name) as {Key.CHAT_NAME}, group_concat(SUBSTRING(first_name, 1, 1), SUBSTRING(first_name, 1, 1)) as {Key.ALT_IMAGE_TEXT} from user "+
                            "where id in ("+
                            "select cm1.user1_id from chat_member cm1 where cm1.user2_id<>%s "+
                            "union "+
                            "select cm2.user2_id from chat_member cm2 where cm2.user1_id<>%s) ", 
                            [session_user_id, session_user_id]
                        )
                        chat_names = Sql.get_all_records_mapped(cursor)
                        response[Key.CHAT_NAME] = chat_names[Key.CHAT_NAME]
                        response[Key.ALT_IMAGE_TEXT] = chat_names[Key.ALT_IMAGE_TEXT]

                    cursor.execute(
                        f"select concat(first_name, ' ', last_name) as {Key.FULLNAME} from user "+
                        "where find_in_set(id, ("+
                        "select concat(user1_id, ',', user2_id) from chat_member where chat_id=%s"+
                        ")) ",
                        [response[Key.CHAT_ID]]
                    )
                    response[Key.MEMBERS] = Sql.get_all_records_mapped(cursor)

                    print(response)
                    return response

            else:
                self.redirect(Url.CHAT_LIST)

        elif user_id:
            chat_id = None

            connection = Sql.get_connection(self, MysqlDB.LEARN_TORNADO1)
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT cm.chat_id as {Key.CHAT_ID} FROM chat_member cm "+
                "WHERE (cm.user1_id=%s and cm.user2_id=%s) or (cm.user2_id=%s and cm.user1_id=%s);",
                [session_user_id, user_id, session_user_id, user_id]
            )
            
            if cursor.rowcount > 0:
                # Chat is already available
                chat_id = cursor.fetchone()[0]
            else:
                # Create new chat
                cursor = connection.cursor()
                cursor.execute("insert into chat(created_by) values(%s)",[session_user_id])

                chat_id = cursor.lastrowid
                if chat_id:
                    cursor = connection.cursor()
                    cursor.execute(
                        "insert into chat_member(chat_id, user1_id, user2_id, user1_joined_at) values(%s, %s, %s, now())",
                        [chat_id, session_user_id, user_id]
                    )

                    if cursor.lastrowid:
                        print(f"Successfully created chat[id:{chat_id}] for users with id:({session_user_id},{user_id})")
                    else:
                        raise RuntimeError(f'Failed to insert new member for chat[id:{chat_id}]')
                else:
                    raise RuntimeError("Failed to create new chat")
                
            if chat_id:
                self.redirect(f'{Url.CHAT}?{Key.CHAT_ID}={chat_id}')
            else:
                self.redirect(Url.CHAT)
        
        else:
            print("Showing chat list...")
            self.render(ChatHtmlFile, **response)


# WebSocket handler to handle real-time chat messages
class ChatWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        # When a new WebSocket connection is established
        print("New client connected")
        connected_clients.append(self)

    def on_message(self, message):
        # When a message is received from a WebSocket client
        print("Received message:", message)

        # Broadcast the message to all connected clients
        for client in connected_clients:
            client.write_message(message)

    def on_close(self):
        # When a WebSocket connection is closed
        print("Client disconnected")
        connected_clients.remove(self)
