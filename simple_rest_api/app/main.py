import falcon
from simple_rest_api.app.controller.app_controller import AppController
from waitress import serve

from simple_rest_api.app.exception.exception import CustomException

app = falcon.App(media_type=falcon.MEDIA_JSON)

controller = AppController()
app.add_route('/users/{email}',controller)
app.add_route('/users',controller)
app.add_error_handler(CustomException, controller.custom_exception_handler)


# if __name__ == '__main__':
#     serve(app,127.0.0.1,8000)
