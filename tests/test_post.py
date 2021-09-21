import pytest
from .fixtures import client, user_token_factory_test, use_test_db_fixture, post_user_for_test, session_for_test, post_factory_for_test, post_second_user_for_test
import firebase_admin

# @pytest.mark.usefixtures('use_test_db_fixture')
# class TestPost:

#     def test_create_post(use_test_db_fixture, user_token_factory_test, post_user_for_test):
#         """
#         画像の採点投稿
#         """
#         img: str = "test_img"
#         token: str = user_token_factory_test()

#         res = client.post('/api/v1/scoring', headers={
#             "Authorization": f"Bearer { token }"
#         }, json={
#             "image_url": img
#         })
#         if res.status_code == 400:
#             assert res.json()['detail'] == "image_url's type is wrong"
#         else:
#             assert res.status_code == 200
#             res_json = res.json()
#             assert res_json['user'] == post_user_for_test
#             assert res_json['img'] == img

#     def test_create_post_without_auth(use_test_db_fixture):
#         """
#         認証無しで画像投稿
#         """
#         img: str = "test_img"

#         res = client.post('/api/v1/scoring', json={
#             "image_url": img
#         })

#         assert res.status_code == 403


#     def test_get_empty_users_post(use_test_db_fixture, post_user_for_test, user_token_factory_test):
#         """
#         何も投稿していないユーザーの投稿画像の取得
#         """

#         user_num = 0
#         token: str = user_token_factory_test(user_num)

#         res = client.get('/api/v1/posts/me', headers={
#             "Authorization": f"Bearer { token }"
#         })

#         assert res.status_code == 200
#         res_json = res.json()
#         assert res_json == []

#     def test_get_users_post(use_test_db_fixture, post_user_for_test, user_token_factory_test, post_factory_for_test):
#         """
#         ユーザーの投稿画像の取得
#         """

#         user_num = 0
#         test_post_list = [
#             {
#                 "point": 100,
#                 "image_url": "https://example.com/hoge.jpg"
#             },
#             {
#                 "point": 300,
#                 "image_url": "https://example.com/fuga.png"
#             }
#         ]
#         token: str = user_token_factory_test(user_num)
#         post_factory_for_test(user_num, test_post_list[1]['point'], test_post_list[1]['image_url'])
#         post_factory_for_test(user_num, test_post_list[0]['point'], test_post_list[0]['image_url'])

#         res = client.get('/api/v1/posts/me', headers={
#             "Authorization": f"Bearer { token }"
#         })

#         assert res.status_code == 200
#         res_json = res.json()
#         assert len(res_json) == len(test_post_list)
#         for res_post, test_post in zip(res_json, test_post_list):
#             assert res_post['point'] == test_post['point']
#             assert res_post['image_url'] == test_post['image_url']

#     def test_get_users_post_without_auth(use_test_db_fixture):
#         """
#         認証無しでユーザーの投稿画像の取得
#         """

#         res = client.get('/api/v1/posts/me')

#         assert res.status_code == 403

#     def test_get_post_ranking(use_test_db_fixture, user_token_factory_test, post_user_for_test, post_factory_for_test):
#         """
#         ランキングを取得する
#         """
#         token = user_token_factory_test()
#         test_post = {
#             "point": 300,
#             "image_url": "hoge.com/hoge.png"
#         }
#         post_factory_for_test(point=test_post["point"], image_url=test_post["image_url"])

#         res = client.get('/api/v1/ranking/posts', headers={
#             "Authorization": f"Bearer { token }"
#         })

#         assert res.status_code == 200
#         res_json = res.json()
#         res_post = res_json[0]
#         assert res_post["point"] == test_post["point"]
#         assert res_post["image_url"] == test_post["image_url"]

#     def test_get_post_ranking_change_top(use_test_db_fixture, user_token_factory_test, post_user_for_test, post_factory_for_test):
#         """
#         ランキングの1位を塗り替える
#         """
#         token = user_token_factory_test()
#         test_posts = [
#             {
#                 "point": 300,
#                 "image_url": "hoge.com/hoge.png"
#             },
#             {
#                 "point": 500,
#                 "image_url": "hoge.com/fuga.png"
#             }
#         ]

#         post_factory_for_test(point=test_posts[0]["point"], image_url=test_posts[0]["image_url"])

#         res = client.get('/api/v1/ranking/posts', headers={
#             "Authorization": f"Bearer { token }"
#         })

#         assert res.status_code == 200
#         res_json = res.json()
#         res_post = res_json[0]

#         post_factory_for_test(point=test_posts[1]["point"], image_url=test_posts[1]["image_url"])

#         res = client.get('/api/v1/ranking/posts', headers={
#             "Authorization": f"Bearer { token }"
#         })

#         assert res.status_code == 200
#         res_json = res.json()
#         res_post_after = res_json[0]

#         assert res_post != res_post_after



#     def test_get_empty_post_ranking(use_test_db_fixture, user_token_factory_test, post_user_for_test):
#         token = user_token_factory_test()

#         res = client.get('/api/v1/ranking/posts', headers={
#             "Authorization": f"Bearer { token }"
#         })

#         assert res.status_code == 200
#         res_json = res.json()
#         assert res_json == []

#     def test_get_post_ranking_without_auth(use_test_db_fixture):
#         """
#         認証無しでユーザーの投稿画像の取得
#         """

#         res = client.get('/api/v1/ranking/posts')

#         assert res.status_code == 403

#     def test_delete_post_by_id(use_test_db_fixture, user_token_factory_test, post_user_for_test, post_factory_for_test):
#         """
#         投稿したポストを削除する
#         """
#         token = user_token_factory_test()
#         post = post_factory_for_test()

#         res = client.delete(f'/api/v1/posts/{ post.id }', headers={
#             "Authorization": f"Bearer { token }"
#         })

#         assert res.status_code == 200
#         assert res.json() == True

#     def test_delete_post_missing_id(use_test_db_fixture, user_token_factory_test, post_user_for_test):
#         """
#         存在しないPostのIDを指定して削除する
#         """
#         token = user_token_factory_test()
#         post_id = "hogehoge"

#         res = client.delete(f'/api/v1/posts/{ post_id }', headers={
#             "Authorization": f"Bearer { token }"
#         })

#         assert res.status_code == 400
#         assert res.json()['detail'] == "Post not exist."

#     def test_delete_post_without_auth(use_test_db_fixture, post_user_for_test, post_factory_for_test):
#         post = post_factory_for_test()
#         res = client.delete(f'/api/v1/posts/{ post.id }')

#         assert res.status_code == 403

#     def test_delete_other_user_post(use_test_db_fixture, user_token_factory_test, post_user_for_test, post_second_user_for_test, post_factory_for_test):
#         token = user_token_factory_test(user_num=0)
#         post = post_factory_for_test(user_num=1)

#         res = client.delete(f'/api/v1/posts/{ post.id }', headers={
#             "Authorization": f"Bearer { token }"
#         })

#         assert res.status_code == 400
