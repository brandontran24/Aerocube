from flask import Flask 
import unittest 
import restSample
import requests 
import subprocess

#Make sure to have an image named sampleImage.png on the flaskServer directory in order to run these tests

class RestTestCase(unittest.TestCase):

	def setUp(self):
		restSample.app.config['TESTING'] = True 
		self.app = restSample.app.test_client()

	def tearDown(self):
		subprocess.call(['rm', 'static/img/sampleImage.png'])

	def test_successful_upload(self):
		files = {'photo': open('sampleImage.png', 'rb')}
		response = requests.post("http://127.0.0.1:5000/api/uploadImage", files = files)
		self.assertEqual(response.status_code, 200)
	
	def test_file_existence(self):
		files = {'photo': open('sampleImage.png', 'rb')}
		requests.post("http://127.0.0.1:5000/api/uploadImage", files = files)
		existence = False
		ls_command = subprocess.check_output(['ls','static/img'])
		if 'sampleImage.png' in ls_command:
			existence = True
		self.assertEqual(existence, True)


if __name__ == '__main__':
	unittest.main() 