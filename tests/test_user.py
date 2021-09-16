import pytest
from .fixtures import client, user_token_test, use_test_db_fixture
from cruds.users import get_current_user_id
import firebase_admin

@pytest.mark.usefixtures('use_test_db_fixture')
class TestCreateUser:

    def test_post_user(use_test_db_fixture, user_token_test):
        """
        Workを投稿する
        """
        name: str = "test_username"
        token: str = user_token_test
        id: str = firebase_admin.auth.verify_id_token(token)['user_id']

        res = client.post('/api/v1/signup', headers={
            "Authorization": f"Bearer { token }"
        }, json={
            "name": name
        })

        assert res.status_code == 200
        res_json = res.json()
        assert res_json['id'] == id
        assert res_json['name'] == name

