from django.test import TestCase
from django.contrib.auth import get_user_model
#from urllib.request import urlopen
import requests
import socket
from account.models import User
import time



class UsersManagersTests(TestCase):
    def test_create_valid_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(AttributeError):
            print(user.username)
    def test_create_not_valid_user(self):
        User = get_user_model()
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")
    def test_create_valid_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(AttributeError):
            print(admin_user.username)
    def test_create_not_valid_superuser(self):    
        User = get_user_model()
        with self.assertRaises(TypeError):
            User.objects.create_superuser()
        with self.assertRaises(TypeError):
            User.objects.create_superuser(email='')
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='', password="foo")
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


class ViewSetTests(TestCase):


    def setUp(self):
        self.hostname = socket.gethostname()
        self.IP = socket.gethostbyname(self.hostname)
        self.uri_users = 'http://' + self.IP + ':8000' + '/users/'
        self.uri_auth = 'http://' + self.IP + ':8000' + '/api-token-auth/'
    
    
    def test_GET_of_anonimous(self):
        response = requests.get(self.uri_users)
        self.assertEqual(response.status_code, 401)


    def test_POST_of_anonimous_create_new_user(self):
        response = requests.post(self.uri_users, data={"email":"v1@sas.com", "password":"1"})
        self.assertEqual(response.status_code, 201)
        response = requests.post(self.uri_auth, data={"username":"v1@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})
        

    def test_PUT_of_anonimous(self):
        response = requests.put(self.uri_users)
        self.assertEqual(response.status_code, 405)

    def test_PATCH_of_anonimous(self):
        response = requests.patch(self.uri_users)
        self.assertEqual(response.status_code, 405)

    def test_DELETE_of_anonimous(self):
        response = requests.delete(self.uri_users)
        self.assertEqual(response.status_code, 405)

    def test_POST_get_authorization_token(self):
        response = requests.post(self.uri_users, data={"email":"v1@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"v1@sas.com", "password":"1"})
        self.assertEqual(response.status_code, 200)
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})

    def test_GET_authorized_user(self):
        response = requests.post(self.uri_users, data={"email":"v1@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"v1@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        self.assertEqual(response.status_code, 200)
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})

    def test_POST_authorized_user_create_new_user(self):
        response = requests.post(self.uri_users, data={"email":"v1@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"v1@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.post(self.uri_users, headers={'Authorization': 'token {}'.format(token)}, 
                    data={"email":"v2@sas.com", "password":"1"})
        self.assertEqual(response.status_code, 201)
        response = requests.post(self.uri_auth, data={"username":"v2@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})
        response = requests.post(self.uri_auth, data={"username":"v1@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})

    def test_PUT_authorized_user(self):
        response = requests.post(self.uri_users, data={"email":"v1@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"v1@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.put(uri_user, headers={'Authorization':'token {}'.format(token)}, 
                    data={"email":"v1@sas.com", "password":"1", "first_name":"Boris"})
        self.assertEqual(response.status_code, 200)
        response = requests.post(self.uri_auth, data={"username":"v1@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})


    def test_PATCH_authorized_user(self):
        response = requests.post(self.uri_users, data={"email":"v1@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"v1@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.patch(uri_user, headers={'Authorization':'token {}'.format(token)}, 
                    data={"email":"v1@sas.com", "password":"1", "last_name":"Jhonson"})
        self.assertEqual(response.status_code, 200)
        response = requests.post(self.uri_auth, data={"username":"v1@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})

    def test_DELETE_authorized_user_delete_someself(self):
        response = requests.post(self.uri_users, data={"email":"v3@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"v3@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})
        self.assertEqual(response.status_code, 204)

    def test_DELETE_superuser_delete_of_any_user(self):
        response = requests.post(self.uri_users, data={"email":"v3@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"test@test.com", "password":"password123"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})
        self.assertEqual(response.status_code, 204)

    def test_PUT_superuser_put_of_any_user(self):
        response = requests.post(self.uri_users, data={"email":"v3@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"test@test.com", "password":"password123"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.put(uri_user, headers={'Authorization':'token {}'.format(token)}, 
                    data={"email":"v3@sas.com", "password":"1", "first_name":"Djohn"})
        self.assertEqual(response.status_code, 200)
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})

    def test_PATCH_superuser_patch_of_any_user(self):
        response = requests.post(self.uri_users, data={"email":"v3@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"test@test.com", "password":"password123"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.patch(uri_user, headers={'Authorization':'token {}'.format(token)}, 
                    data={"email":"v3@sas.com", "password":"1", "last_name":"Broun"})
        self.assertEqual(response.status_code, 200)
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})

    def test_GET_superuser_full_info(self):
        response = requests.post(self.uri_users, data={"email":"v1@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"test@test.com", "password":"password123"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        self.assertGreater(len(response.json()), 2)
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})

    def test_GET_authorized_user_get_only_self_info(self):
        response = requests.post(self.uri_users, data={"email":"v1@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"v1@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        self.assertEqual(len(response.json()), 1)
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})
        