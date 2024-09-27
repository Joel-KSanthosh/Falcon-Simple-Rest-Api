from venv import logger

import falcon
from rest.app_controller import ExceptionHandler, UserPost, UserGet
from waitress import serve
import os
from exception.exception import CustomException

current_path = os.curdir
logger.info(current_path)

app = falcon.App(media_type=falcon.MEDIA_JSON)

post_api = UserPost()
get_api = UserGet()
exception_handler = ExceptionHandler()
app.add_route('/users/{email}',get_api)
app.add_route('/users',post_api)
app.add_error_handler(CustomException, exception_handler.custom_exception_handler)


if __name__ == '__main__':
    logger.info("Falcon App is starting")
    serve(app,host="127.0.0.1",port=8000)
