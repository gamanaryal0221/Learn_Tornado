import tornado.web
import tornado.ioloop

from ..utils.constants import Constants
Key = Constants.Key

class ErrorHandler(tornado.web.RequestHandler):
    def get(self):
        error = {
            Key.ERROR_MSG: self.get_argument(Key.ERROR_MSG,'')
        }
        self.render(Constants.HtmlFile.ERROR, **error)