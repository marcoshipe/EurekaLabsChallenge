from secrets import token_urlsafe
from app.crud.crud_user import _encrypt_password
from app.database.database_test import test_db


class TestUsers:
    def test_encrypt_password_short(self, test_db):
        assert _encrypt_password('short') == ''

    def test_encrypt_password_ok(self, test_db):
        api_key = token_urlsafe(12)
        assert _encrypt_password(api_key) != ''
        assert _encrypt_password(api_key) == _encrypt_password(api_key)

    # TODO: Complete with the rest of the tests
