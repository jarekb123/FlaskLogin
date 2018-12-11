from flask import json

from tests.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):
    mock_user = json.dumps(dict(
        email='joe@email.com',
        password='123456'
    ))

    def test_registration(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=self.mock_user,
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_user_login(self):
        with self.client:
            # register user first
            self.client.post(
                'auth/register',
                data=self.mock_user,
                content_type='application/json'
            )
            response_login = self.client.post(
                '/auth/login',
                data=self.mock_user,
                content_type='application/json'
            )
            data = json.loads(response_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response_login.content_type == 'application/json')
            self.assertEqual(response_login.status_code, 200)
