import falcon
from falcon import testing, HTTP_409
import pytest

from rest.app_controller import AppController
from exception.exception import CustomException


@pytest.fixture
def client():
    app = falcon.App()
    controller = AppController()
    add_route('/users', controller)
    add_route('/users/{email}', controller)
    add_error_handler(CustomException, controller.custom_exception_handler)
    return testing.TestClient(app)


def test_get_user_by_email_success(client, mocker):
    mock_user = {'name': 'John Doe', 'email': 'john@example.com', 'age': 30}
    mocker.patch('models.user.User.find_user_with_email', return_value=mock_user)

    response = client.simulate_get('/users/john@example.com')
    assert response.status == falcon.HTTP_200
    assert response.json['message'] == 'Successfully Fetched.'
    assert response.json['data'] == mock_user


def test_get_user_success(client, mocker):
    mock_user = [{'name': 'John Doe', 'email': 'john@example.com', 'age': 30},
                 {'name': 'Joel', 'email': 'joel@example.com', 'age': 22}]
    mocker.patch('models.user.User.find_all_user', return_value=mock_user)

    response = client.simulate_get('/users/')
    assert response.status == falcon.HTTP_200
    assert response.json['message'] == 'Successfully Fetched.'
    assert response.json['data'] == mock_user


def test_get_user_no_user_exists(client, mocker):
    mock_user = []
    mocker.patch('models.user.User.find_all_user', return_value=mock_user)

    response = client.simulate_get('/users/')
    assert response.status == falcon.HTTP_400
    assert response.json['message'] == 'No users exist!'


def test_get_user_by_email_not_found(client, mocker):
    mocker.patch('models.user.User.find_user_with_email', return_value=None)

    response = client.simulate_get('/users/john@example.com')
    assert response.status == falcon.HTTP_400
    assert response.json['message'] == "User with given email doesn't exist!"


def test_create_user_success(client, mocker):
    mock_save = mocker.patch('models.user.User.save', return_value=None)

    response = client.simulate_post('/users', json={'name': 'John Doe', 'email': 'john@example.com', 'age': 30})
    assert response.status == falcon.HTTP_200
    assert response.json['message'] == "Successfully inserted user"
    mock_save.assert_called_once_with('John Doe', 'john@example.com', 30)


def test_create_user_file_not_found(client, mocker):
    mock_save = mocker.patch('models.user.User.save', return_value=None)

    mock_open = mocker.patch('builtins.open', side_effect=FileNotFoundError)

    response = client.simulate_post('/users', json={'name': 'John Doe', 'email': 'john@example.com', 'age': 30})

    assert response.status == falcon.HTTP_200
    assert response.json['message'] == "Successfully inserted user"

    mock_save.assert_called_once_with('John Doe', 'john@example.com', 30)
    assert mock_open.called


def test_create_user_invalid_request_body(client, mocker):
    mocker.patch('models.user.User.save', side_effect=CustomException("Request body is invalid!"))

    response = client.simulate_post('/users',
                                    json={'name': 'John Doe', 'email': 'john@example.com', 'age': 30, 'dark': 'hehe'})
    assert response.status == falcon.HTTP_400
    assert response.json['message'] == "Request body is invalid!"


def test_create_user_invalid_email(client, mocker):
    mocker.patch('models.user.User.save', side_effect=CustomException("Enter a valid email!"))

    response = client.simulate_post('/users', json={'name': 'John Doe', 'email': 'invalid_email', 'age': 30})
    assert response.status == falcon.HTTP_400
    assert response.json['message'] == "Enter a valid email!"


def test_create_user_invalid_key(client, mocker):
    mocker.patch('models.user.User.save')

    response = client.simulate_post('/users', json={'name': 'John Doe', 'emfail': 'john@example.com', 'age': 30})
    assert response.status == falcon.HTTP_400
    assert 'is required!' in response.json['message']


def test_create_user_duplicate_email(client, mocker):
    mocker.patch('models.user.User.save',
                 side_effect=CustomException("Email already exist!", HTTP_409))

    response = client.simulate_post('/users', json={'name': 'John Doe', 'email': 'john@example.com', 'age': 30})
    assert response.status == falcon.HTTP_409
    assert response.json['message'] == "Email already exist!"
