from django.test import TestCase
from django.contrib.auth import get_user_model
import requests
import socket
from django.conf import settings
from django.db import models
import django.utils.timezone

from account.models import User
from account.managers import CustomUserManager


class AdvertFileViewSetTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.hostname = socket.gethostname()
        cls.IP = socket.gethostbyname(cls.hostname)
        cls.uri_advert_file = 'http://' + cls.IP + ':8000' + '/advertfile/'
#        cls.uri_auth = 'http://' + cls.IP + ':8000' + '/api-token-auth/'
    
    
#    def test_GET_of_anonimous(self):
#        response = requests.get(self.uri_users)
#        self.assertEqual(response.status_code, 401)


    def test_POST_of_anonimous_upload_file(self):
        files = {'advert_file': open('C:/gitone/MyBmp_1.bmp', 'rb')}
        data = {"advert_id": "1"}
        response = requests.post(self.uri_advert_file, files=files, data=data)
        print(response.json())
        self.assertEqual(response.status_code, 201)
