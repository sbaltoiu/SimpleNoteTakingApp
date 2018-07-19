# tests.py

import unittest
import os

from flask import abort, url_for
from flask_testing import TestCase
from app import create_app, db
from app.models import User, Note

class TestBase(unittest.TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://admin:dt2016@localhost/simplenoteapp_test'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = User(username="admin", password="admin2016", is_admin=True)

        # create test non-admin user
        employee = User(username="test_user", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
