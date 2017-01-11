from flask import Flask
import unittest
import requests
import subprocess
import os
import flaskServer.restEndpoint as restEndpoint
from .settings import FlaskServerSettings


class TestRestEndpoint(unittest.TestCase):
    """
    TODO: fails unless the controller is also running
    Make sure _test_img has the name (as a str) of an existing file
    in the designated test_file dir.
    """
    _test_img = 'ucsb_logo.jpg'
    _static_img_dir = FlaskServerSettings.get_static_img_dir()
    _test_img_path = os.path.join(FlaskServerSettings.get_test_files_dir(), _test_img)
    _static_img_path = os.path.join(FlaskServerSettings.get_static_img_dir(), _test_img)

    def setUp(self):
        restEndpoint.app.config['TESTING'] = True
        self.app = restEndpoint.app.test_client()

    def tearDown(self):
        subprocess.call(['rm', self._static_img_path])

    def test_successful_upload(self):
        files = {'photo': open(self._test_img_path, 'rb')}
        response = requests.post('http://127.0.0.1:5005/api/uploadImage', files=files)
        self.assertEqual(response.status_code, 200)

    def test_file_existence(self):
        files = {'photo': open(self._test_img_path, 'rb')}
        ls_command = subprocess.getoutput('ls ' + self._static_img_dir)
        self.assertFalse(self._test_img in ls_command.split('\n'),
                         msg='Precondition: {0} image should not exist at the API image upload endpoint.'.format(self._test_img))
        requests.post('http://127.0.0.1:5005/api/uploadImage', files=files)
        ls_command = subprocess.getoutput('ls ' + self._static_img_dir)
        self.assertTrue(self._test_img in ls_command.split('\n'),
                        msg='Postcondition: {0} was not sucessfully created at the API image upload endpoint.'.format(self._test_img))


if __name__ == '__main__':
    unittest.main()