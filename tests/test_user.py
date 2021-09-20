import pytest
from .fixtures import client, user_token_test, use_test_db_fixture, post_user_for_test, session_for_test
import firebase_admin

@pytest.mark.usefixtures('use_test_db_fixture')
class TestCreateUser:

    def test_post_user(use_test_db_fixture, user_token_test):
        """
        ユーザーを登録する
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

    def test_post_already_user(use_test_db_fixture, user_token_test, post_user_for_test):
        """
        すでに登録されているユーザーを登録する
        """
        name: str = post_user_for_test.name
        token: str = user_token_test
        res = client.post('/api/v1/signup', headers={
            "Authorization": f"Bearer { token }"
        }, json={
            "name": name
        })

        assert res.status_code == 400 

    def fixture_get_user(use_test_db_fixture, user_token_test, post_user_for_test):
        """
        ユーザー情報の取得
        """
        name: str = post_user_for_test.name
        token: str = user_token_test
        id: str = post_user_for_test.id

        res = client.get('/api/v1/users/me', headers={
            "Authorization": f"Bearer { token }"
        })

        assert res.status_code == 200
        res_json = res.json()
        assert res_json['id'] == id
        assert res_json['name'] == name

