#!/usr/bin/env python3

# Author: Eugene Egbe
# Unit tests for the routes

import json
import unittest
from tool import app


class TestUser(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()


    def tearDown(self):
        pass

    def test_current_user_not_logged_in_outputs_redirect_status_code(self):
        res = self.app.get('/login')
        self.assertEqual(res.status_code, 302)

    def test_current_user_not_logged_in_returns_message(self):
        res = self.app.get('/api/v1/current_user')
        expected  = {'message': 'User not logged in', 'status': 'failure'}
        self.assertDictEqual(json.loads(res.data), expected)


if __name__ == '__main__':
    unittest.main()
