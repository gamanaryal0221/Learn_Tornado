import tornado.ioloop
import tornado.web

# Configurations
import main.config.setting as setting

# mysql db connection
import main.connection.mysql as mysql

# firebase connection
import main.connection.firebase as firebase

# Url Mapping
import main.src.code.url.url_mapping as url

from main.src.code.utils.constants import Constants


def make_app():
    app = tornado.web.Application(
        url.get_all_mappings(),
        debug=True,
        autoreload=True
    )

    config = setting.read_configuration()

    cookie_key = Constants.COOKIE_SECRET_KEY
    cookie_secret_key = config[cookie_key] if cookie_key in config else None
    app.settings[cookie_key] = cookie_secret_key
    print(f'\nCoookie secret key has been set successfully')

    app.settings[Constants.TEMPLATE_PATH_KEY] = Constants.TEMPLATE_PATH
    print(f'\nTemplate path = {Constants.TEMPLATE_PATH}')

    app.token_detail = setting.get_token_detail(config)
    app.mysql_connections = mysql.get_connections(config)
    firebase.initialize(config)

    return app


if __name__ == "__main__":
    print('\n===================== Initializing =====================')
    app = make_app()

    port  = 8888
    app.listen(port)

    # Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    # C:\Apache24\bin\httpd.exe
    # /user/(?P<action>create|list|profile|edit|delete)
    print(f'\nServer is live on http://localhost:8888')
    tornado.ioloop.IOLoop.instance().start()