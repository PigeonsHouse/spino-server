import pytest
from .fixtures import client, user_token_factory_test, use_test_db_fixture, post_user_for_test, session_for_test, post_factory_for_test, post_second_user_for_test
import firebase_admin

@pytest.mark.usefixtures('use_test_db_fixture')
class TestUser:

    def test_post_user(use_test_db_fixture, user_token_factory_test):
        """
        ユーザーを登録する
        """
        name: str = "test_username"
        img: str = "test_img"
        token: str = user_token_factory_test()
        id: str = firebase_admin.auth.verify_id_token(token)['user_id']

        res = client.post('/api/v1/signup', headers={
            "Authorization": f"Bearer { token }"
        }, json={
            "name": name,
            "img": img
        })

        assert res.status_code == 200
        res_json = res.json()
        assert res_json['id'] == id
        assert res_json['name'] == name
        assert res_json['img'] == img


    def test_post_already_user(use_test_db_fixture, user_token_factory_test, post_user_for_test):
        """
        すでに登録されているユーザーを登録する
        """
        name: str = post_user_for_test.name
        img: str = post_user_for_test.img
        token: str = user_token_factory_test()
        res = client.post('/api/v1/signup', headers={
            "Authorization": f"Bearer { token }"
        }, json={
            "name": name,
            "img": img
        })

        assert res.status_code == 400 

    def test_get_user(use_test_db_fixture, user_token_factory_test, post_user_for_test):
        """
        ユーザー情報の取得
        """
        name: str = post_user_for_test.name
        img: str = post_user_for_test.img
        token: str = user_token_factory_test()
        id: str = post_user_for_test.id

        res = client.get('/api/v1/users/me', headers={
            "Authorization": f"Bearer { token }"
        })

        assert res.status_code == 200
        res_json = res.json()
        assert res_json['id'] == id
        assert res_json['name'] == name
        assert res_json['img'] == img

    def test_get_user_without_auth(use_test_db_fixture, post_user_for_test):
        """
        認証無しでユーザー情報の取得
        """
        res = client.get('/api/v1/users/me')

        assert res.status_code == 403


    def test_change_user_info(use_test_db_fixture, user_token_factory_test, post_user_for_test):
        """
        ユーザー情報の変更
        """
        test_name_1 = "test_name_first"
        test_img_1 = "test_image_first"
        test_name_2 = "test_name_second"
        test_img_2 = "test_image_second"
        img: str = post_user_for_test.img
        user_id: str = post_user_for_test.id
        token: str = user_token_factory_test()

        res = client.put('/api/v1/signup', headers={
            "Authorization": f"Bearer { token }"
        }, json={
            "name": test_name_1
        })
        assert res.status_code == 200
        res_json = res.json()
        assert res_json['id'] == user_id
        assert res_json['name'] == test_name_1
        assert res_json['img'] == img

        res = client.put('/api/v1/signup', headers={
            "Authorization": f"Bearer { token }"
        }, json={
            "img": test_img_1
        })
        assert res.status_code == 200
        res_json = res.json()
        assert res_json['id'] == user_id
        assert res_json['name'] == test_name_1
        assert res_json['img'] == test_img_1

        res = client.put('/api/v1/signup', headers={
            "Authorization": f"Bearer { token }"
        }, json={
            "name": test_name_2,
            "img": test_img_2
        })
        assert res.status_code == 200
        res_json = res.json()
        assert res_json['id'] == user_id
        assert res_json['name'] == test_name_2
        assert res_json['img'] == test_img_2

    def test_change_info_without_signup(use_test_db_fixture, user_token_factory_test):
        """
        サインアップしていないユーザーの情報を変更する
        """
        test_name = "test_name_first"
        test_img = "test_image_first"
        token: str = user_token_factory_test()

        res = client.put('/api/v1/signup', headers={
            "Authorization": f"Bearer { token }"
        }, json={
            "name": test_name,
            "img": test_img
        })

        assert res.status_code == 400

    def test_change_info_without_auth(use_test_db_fixture):
        """
        認証無しでユーザーの情報を変更する
        """
        test_name = "test_name_first"
        test_img = "test_image_first"

        res = client.put('/api/v1/signup', json={
            "name": test_name,
            "img": test_img
        })
        assert res.status_code == 403

    def test_get_user_ranking(use_test_db_fixture, post_user_for_test, user_token_factory_test, post_factory_for_test):
        """
        ユーザーランキングの取得
        """
        post = post_factory_for_test(point=300, image_url="hoge")
        token = user_token_factory_test()

        res = client.get('/api/v1/ranking/users', headers={
            "Authorization": f"Bearer { token }"
        })

        assert res.status_code == 200
        res_json = res.json()
        assert res_json[0]['id'] == post_user_for_test.id

    def test_get_user_ranking_overlapping(use_test_db_fixture, post_user_for_test, post_second_user_for_test, user_token_factory_test, post_factory_for_test):
        """
        同一ユーザーの上書きを試しつつユーザーランキングの取得
        """
        post_factory_for_test(point=300, image_url="hoge")
        post_factory_for_test(point=400, image_url="fuga")
        token = user_token_factory_test()

        res = client.get('/api/v1/ranking/users', headers={
            "Authorization": f"Bearer { token }"
        })

        assert res.status_code == 200
        res_json = res.json()
        assert len(res_json) == 1

        post_factory_for_test(user_num=1, point=400, image_url="fuga")

        res = client.get('/api/v1/ranking/users', headers={
            "Authorization": f"Bearer { token }"
        })

        assert res.status_code == 200
        res_json = res.json()
        assert len(res_json) == 2

    def test_get_empty_user_ranking(use_test_db_fixture, post_user_for_test, user_token_factory_test):
        token = user_token_factory_test()

        res = client.get('/api/v1/ranking/users', headers={
            "Authorization": f"Bearer { token }"
        })

        assert res.status_code == 200
        res_json = res.json()
        assert res_json == []

    def test_get_user_ranking_without_auth(use_test_db_fixture):
        res = client.get('/api/v1/ranking/users')

        assert res.status_code == 403

    def test_get_user_ranking_with_delete(use_test_db_fixture, user_token_factory_test, post_user_for_test, post_second_user_for_test, post_factory_for_test):
        """
        投稿を削除しつつユーザーランキングを取得する
        """
        first_high_score = 50
        second_high_score = 30
        third_high_score = 10

        token_1 = user_token_factory_test(user_num=0)
        token_2 = user_token_factory_test(user_num=1)

        post_1_low = post_factory_for_test(user_num=0, point=third_high_score)
        post_2 = post_factory_for_test(user_num=1, point=second_high_score)
        post_1_high = post_factory_for_test(user_num=0, point=first_high_score)

        res = client.get('/api/v1/ranking/users', headers={
            "Authorization": f"Bearer { token_1 }"
        })

        assert res.status_code == 200
        res_json = res.json()

        assert len(res_json) == 2
        assert res_json[0]['id'] == post_user_for_test.id
        assert res_json[0]['high_score'] == first_high_score


        res = client.delete(f'/api/v1/posts/{ post_1_high.id }', headers={
            "Authorization": f"Bearer { token_1 }"
        })

        assert res.status_code == 200
        assert res.json() == True


        res = client.get('/api/v1/ranking/users', headers={
            "Authorization": f"Bearer { token_1 }"
        })

        assert res.status_code == 200
        res_json = res.json()

        assert len(res_json) == 2
        assert res_json[0]['id'] == post_second_user_for_test.id
        assert res_json[0]['high_score'] == second_high_score


        res = client.delete(f'/api/v1/posts/{ post_2.id }', headers={
            "Authorization": f"Bearer { token_2 }"
        })

        assert res.status_code == 200
        assert res.json() == True


        res = client.get('/api/v1/ranking/users', headers={
            "Authorization": f"Bearer { token_1 }"
        })

        assert res.status_code == 200
        res_json = res.json()

        assert len(res_json) == 1
        assert res_json[0]['id'] == post_user_for_test.id
        assert res_json[0]['high_score'] == third_high_score
