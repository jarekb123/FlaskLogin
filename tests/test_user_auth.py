from flask import json

from tests.base import BaseTestCase

json_content = "application/json"

class TestAuthBlueprint(BaseTestCase):
    mock_user = json.dumps(dict(
        email='joe@email.com',
        password='123456'
    ))

    def test_registration(self):
        with self.client:
            response = self.client.post(
                '/user/register',
                data=self.mock_user,
                content_type=json_content
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.content_type, json_content)
            self.assertEqual(response.status_code, 201)

    def test_registration_already_created_user(self):
        with self.client:
            # user not registered yet - register one
            self.client.post(
                '/user/register',
                data=self.mock_user,
                content_type=json_content
            )
            # try to register again
            response = self.client.post(
                '/user/register',
                data=self.mock_user,
                content_type=json_content
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'],'user_already_exist')
            self.assertEqual(response.content_type, json_content)
            self.assertEqual(response.status_code, 202)

    def test_registered_user_login(self):
        with self.client:
            # register user first
            self.client.post(
                'user/register',
                data=self.mock_user,
                content_type=json_content
            )
            response_login = self.client.post(
                '/user/login',
                data=self.mock_user,
                content_type=json_content
            )
            data = json.loads(response_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response_login.content_type, json_content)
            self.assert200(response_login)

    def test_unregistered_user_login(self):
        with self.client:
            response = self.client.post(
                '/user/login',
                data=self.mock_user,
                content_type=json_content
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(response.content_type, json_content)
            self.assert500(response)

    def test_valid_logout(self):
        """ Test for logout before token expires """
        with self.client:
            # registration
            self.client.post(
                'user/register',
                data=self.mock_user,
                content_type=json_content
            )
            # login
            login_resp = self.client.post(
                'user/login',
                data=self.mock_user,
                content_type=json_content
            )
            login_resp_data = json.loads(login_resp.data.decode())
            # logout
            logout_response = self.client.get(
                'user/logout',
                headers=dict(
                    Authorization='Bearer ' + login_resp_data['auth_token']
                )
            )
            logout_data = json.loads(logout_response.data.decode())
            self.assertEqual(logout_data['status'], 'success')
            self.assertEqual(logout_response.status_code, 200)
