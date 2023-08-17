import os
BASE_LOCATION = os.getcwd()


class Constants():
    TEMPLATE_PATH_KEY = 'template_path'
    TEMPLATE_PATH = BASE_LOCATION + '\main\src\\templates'

    STATIC_PATH_KEY = 'path'
    STATIC_PATH = BASE_LOCATION + '\main\src\static'

    COOKIE_SECRET_KEY = 'cookie_secret'

    PASSWORD_ENCODING_STANDARD = 'utf-8'

    MALE = 1
    FEMALE = 0

    class Config():
        LOCATION = BASE_LOCATION + '\main\config'
        FILE_NAME = 'configuration.json'

        class Key():
            MYSQL_DATA_SOURCES = 'data_sources'
            FIREBASE = 'firebase'
            TOKEN = 'token'

        class Token():
            PRIVATE_KEY = 'private_key'
            EXPIRE_DURATION = 'expire_duration'
            ALGORITHM = 'algorithm'

            DEFAULT_EXPIRE_DURATION = 8
            DEFAULT_ALGORITHM = 'HS256'

        class MysqlDB():
            LEARN_TORNADO1 = 'learn_tornado1'
            LEARN_TORNADO2 = 'learn_tornado2'

            HOSTNAME = 'hostname'
            DATABASE = 'database'
            USER = 'user'
            PASSWORD = 'password'

        class Firebase():
            DB_URL = 'db_url'
            
    class FirebaseAccountKey():
        LOCATION = BASE_LOCATION + '\main\config\\firebase'
        FILE_NAME = 'service_account_key.json'

    class RequestMethod():
        GET = 'get'

    class HtmlFile():
        HOME = 'home.html'
        REGISTRATION = 'registration.html'
        LOGIN = 'login.html'
        CHAT = 'chats.html'
        ERROR = 'error.html'
        USERS = 'user/users.html'
        CLIENTS = 'client/clients.html'

    class Url():
        HOME = '/'
        STATIC = '/static/(.*)'
        REGISTRATION = '/register'
        LOGIN = '/login'
        LOGOUT = '/logout'
        CHAT_LIST = '/chat/list'
        CHAT = '/chats'
        USERS = '/users'
        ERROR = '/error'
        CLIENTS = '/clients'

        DEFAULT_MALE_PHOTO = 'https://www.ijaist.com/wp-content/uploads/2018/02/default-male-photo.png'
        DEFAULT_FEMALE_PHOTO = 'https://cdn4.vectorstock.com/i/1000x1000/52/83/default-placeholder-profile-icon-vector-14065283.jpg'

        DEFAULT_UM_LOGO = 'https://nationalparks-15bc7.kxcdn.com/images/parks/sagarmatha/20210211212941-Sagarmatha%20National%20Park.jpg?width=1170&height=360'

    class Key():
        ID = 'id'
        USER_ID = 'user_id'
        FIRST_NAME = 'first_name'
        MIDDLE_NAME = 'middle_name'
        LAST_NAME = 'last_name'
        FULLNAME = 'fullname'
        GENDER = 'gender'
        MY_FULLNAME = 'my_fullname'
        PHOTO_URL = 'photo_url'
        EMAIL = 'email'
        NUMBER = 'number'
        EMAIL_OR_NUMBER = 'email_or_number'
        PASSWORD = 'password'
        ERROR_MSG = 'error_msg'
        CHAT_ID = 'chat_id'
        CHAT_NAME = 'chat_name'
        ALT_IMAGE_TEXT = 'alt_image_text'
        USER_LIST = 'user_list'
        EXPIRE_ON = 'exp'
        TOKEN = 'token'
        PAYLOAD = 'payload'
        IS_GROUP_CHAT = 'is_group_chat'
        MEMBERS = 'members'
        IS_ADMIN = 'is_admin'
        JOINED_AT = 'joined_at'
        ADDED_BY = 'added_by'
        SALT_VALUE = 'salt_value'
        HASHED_PASSWORD = 'hashed_password'
        PAGE_URL = 'page_url'
        HOST = 'host'
        CLIENT_ID = 'client_id'
        NAME = 'name'
        DISPLAY_NAME = 'display_name'
        CLIENT_LIST = 'client_list'


    

