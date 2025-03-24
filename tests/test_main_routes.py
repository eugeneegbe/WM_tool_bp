#!/usr/bin/env python3

# Author: Eugene Egbe
# Unit tests for the routes

import unittest
from tool import app


class TestMain(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()


    def tearDown(self):
        pass

    def test_home_route_returns_success(self):
        res = self.app.get('/', follow_redirects=True)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
