import unittest
from unittest.mock import patch
from Healthy.healthy import check_security_health, process
from flask import Flask, request
from flask.json import jsonify
from Healthy.healthy import app


class TestCheckHealth(unittest.TestCase):
    @patch('Healthy.healthy.check_security_health')
    def test_check_health(self, mock_check_package):
        # Arrange
        packages = ['adea', 'json5', "table"]
        mock_check_package.return_value = {'name': 'status'}
        # Act
        result = check_security_health(packages)
        # Assert
        self.assertEqual(result,
                         {
                             'adea': "Package not found",
                             'json5': "Package is healthy",
                             'table': "package unhealthy due to -Last version is more than 30 days old "
                                      "and Latest commit is more than 14 days old"
                         }
                         )


class ProcessTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_process_with_valid_packages(self):
        # Test with valid packages
        data = {'packages': ['json5', 'table']}
        response = self.app.post('/process', json=data)
        self.assertEqual(response.status_code, 200)

    def test_process_with_too_many_packages(self):
        # Test with too many packages
        data = {'packages': [f'package{i}' for i in range(12)]}
        response = self.app.post('/process', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], 'You can only process 10 packages at a time')



if __name__ == '__main__':
    unittest.main()
