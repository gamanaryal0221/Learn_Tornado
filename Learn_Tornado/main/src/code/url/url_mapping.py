import re

import tornado.web
from ..utils.constants import Constants
Url = Constants.Url

from ..handlers.home import HomeHandler, LogoutHandler
from ..handlers.register_login.registration import RegistrationHandler
from ..handlers.register_login.login import LoginHandler
from ..handlers.chat.chat import ChatListHandler, ChatHandler, ChatWebSocketHandler
from ..handlers.user import UserHandler
from ..handlers.client import ClientListHandler
from ..handlers.error import ErrorHandler

from ..verification import EmailUsingSqlHandler, EmailUsingFirebaseHandler

def get_all_mappings():
    print('\n\n---------- Initializing url -> handlers ----------')

    static_path = Constants.STATIC_PATH
    print(f'Static path = {static_path}\n')

    handlers = [
        (fr"{Url.HOME}", HomeHandler),
        (fr"{Url.STATIC}", tornado.web.StaticFileHandler, {Constants.STATIC_PATH_KEY: static_path}),
        (fr"{Url.REGISTRATION}", RegistrationHandler),
        (fr"{Url.LOGIN}", LoginHandler),
        (fr"{Url.LOGOUT}", LogoutHandler),
        (fr"{Url.USERS}",UserHandler),
        (fr"{Url.CLIENTS}",ClientListHandler),
        (fr"{Url.CHAT}",ChatHandler),
        (fr"{Url.ERROR}",ErrorHandler),
        (r"/chat/websocket", ChatWebSocketHandler),
        
        (r"/verify/sql/email", EmailUsingSqlHandler),        
        (r"/verify/firebase/email", EmailUsingFirebaseHandler),
    ]

    for i, handler in enumerate(handlers):
        print(f'{i+1}. {handler[0]} -> {get_handler_name(handler[1])}')

    return handlers

def get_handler_name(_class):
    class_name = re.search(r"'(.*?)'", str(_class)).group(1)
    return str(class_name)
