from fastapi.testclient import TestClient
from app.main import app
from app.database.database_test import test_db


class TestUsers:
    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)

    def test_create_ok(self, test_db):
        data = {'name': 'test_name', 'last_name': 'test_last_name', 'email': 'test_email@gmail.com'}
        response = self.client.post('/users/', json=data)
        assert response.status_code == 200
        assert 'api_key' in response.json()
        assert type(response.json()['api_key']) == str

    def test_create_wrong_email(self, test_db):
        data = {'name': 'test_name', 'last_name': 'test_last_name', 'email': 'test_email'}
        response = self.client.post('/users/', json=data)
        assert response.status_code == 422
        assert response.json() == {'detail': [{'loc': ['body', 'email'], 'msg': 'value is not a valid email address',
                                               'type': 'value_error.email'}]}

    def test_create_no_name(self, test_db):
        data = {'last_name': 'test_last_name', 'email': 'test_email@gmail.com'}
        response = self.client.post('/users/', json=data)
        assert response.status_code == 422
        assert response.json() == {'detail': [{'loc': ['body', 'name'], 'msg': 'field required',
                                               'type': 'value_error.missing'}]}

    def test_create_already_exist(self, test_db):
        data = {'name': 'test_name', 'last_name': 'test_last_name', 'email': 'test_email@gmail.com'}
        self.client.post('/users/', json=data)
        response = self.client.post('/users/', json=data)
        assert response.status_code == 400
        assert response.json() == {'detail': 'Email already registered'}
