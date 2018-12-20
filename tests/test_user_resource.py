from flask import json

from tests.base import BaseTestCase
from user.models import User
from webapp import db


class TestUsersResource(BaseTestCase):

    def test_get_user_data(self):
        with self.client:
            user = User(
                email="email@email.com",
                password="password",
                language="en_US",
                phone="123456789"
            )
            db.session.add(user)
            db.session.commit()

            token = user.encode_auth_token(user.id)

            response = self.client.get(
                '/user/me',
                headers=dict(
                    Authorization='Bearer ' + token.decode()
                )
            )
            data = json.loads(response.data.decode())
            self.assert200(response)
            self.assertEqual(data['email'], 'email@email.com')
            self.assertEqual(data['phone'], '123456789')
