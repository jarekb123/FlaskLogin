from flask_testing import TestCase
from webapp.app import app


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('webapp.config.TestConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'secret_key')
        self.assertTrue(app.config['DEBUG'])
