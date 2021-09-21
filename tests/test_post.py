import pytest
from .fixtures import client, user_token_factory_test, use_test_db_fixture, post_user_for_test, session_for_test, post_factory_for_test
import firebase_admin

@pytest.mark.usefixtures('use_test_db_fixture')
class TestPost:

    def test_create_post(use_test_db_fixture, user_token_factory_test, post_user_for_test):
        """
        画像の採点投稿
        """
        img: str = "test_img"
        token: str = user_token_factory_test()

        res = client.post('/api/v1/scoring', headers={
            "Authorization": f"Bearer { token }"
        }, json={
            "image_url": img
        })
        if res.status_code != 400:
            assert res.status_code == 200
            res_json = res.json()
            assert res_json['user'] == post_user_for_test
            assert res_json['img'] == img
        else:
            assert res.status_code == 400


    def test_get_users_post(use_test_db_fixture, post_user_for_test, user_token_factory_test, post_factory_for_test):
        """
        ユーザーの投稿画像の取得
        """

        user_num = 0
        test_post_list = [
            {
                "point": 100,
                "image_url": "https://example.com/hoge.jpg"
            },
            {
                "point": 300,
                "image_url": "https://example.com/fuga.png"
            }
        ]
        token: str = user_token_factory_test(user_num)
        post_factory_for_test(user_num, test_post_list[0]['point'], test_post_list[0]['image_url'])
        post_factory_for_test(user_num, test_post_list[1]['point'], test_post_list[1]['image_url'])

        res = client.get('/api/v1/posts/me', headers={
            "Authorization": f"Bearer { token }"
        })

        assert res.status_code == 200
        res_json = res.json()
        assert len(res_json) == len(test_post_list)
        for i, post in enumerate(res_json):
            assert post['point'] == test_post_list[i]['point']
            assert post['image_url'] == test_post_list[i]['image_url']