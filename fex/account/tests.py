from django.test import TestCase
from django.contrib.auth import get_user_model
import requests
import socket
from account.models import User
#import time
from django.conf import settings
from django.db import models
import django.utils.timezone
from account.managers import CustomUserManager



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

    @classmethod
    def setUpTestData(cls):
        cls.hostname = socket.gethostname()
        cls.IP = socket.gethostbyname(cls.hostname)
        cls.uri_users = 'http://' + cls.IP + ':8000' + '/users/'
        cls.uri_auth = 'http://' + cls.IP + ':8000' + '/api-token-auth/'
    
    
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
        response = requests.post(self.uri_users, data={"email":"v2@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"v2@sas.com", "password":"1"})
        self.assertEqual(response.status_code, 200)
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})

    def test_GET_authorized_user(self):
        response = requests.post(self.uri_users, data={"email":"v3@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"v3@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        self.assertEqual(response.status_code, 200)
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})

    def test_POST_authorized_user_create_new_user(self):
        response = requests.post(self.uri_users, data={"email":"v4@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"v4@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.post(self.uri_users, headers={'Authorization': 'token {}'.format(token)}, 
                    data={"email":"v4_1@sas.com", "password":"1"})
        self.assertEqual(response.status_code, 201)
        response = requests.post(self.uri_auth, data={"username":"v4_1@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})
        response = requests.post(self.uri_auth, data={"username":"v4@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})

    def test_PUT_authorized_user(self):
        response = requests.post(self.uri_users, data={"email":"v5@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"v5@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.put(uri_user, headers={'Authorization':'token {}'.format(token)}, 
                    data={"email":"v5@sas.com", "password":"1", "first_name":"Boris"})
        self.assertEqual(response.status_code, 200)
        response = requests.post(self.uri_auth, data={"username":"v5@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})


    def test_PATCH_authorized_user(self):
        response = requests.post(self.uri_users, data={"email":"v6@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"v6@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.patch(uri_user, headers={'Authorization':'token {}'.format(token)}, 
                    data={"email":"v6@sas.com", "password":"1", "last_name":"Jhonson"})
        self.assertEqual(response.status_code, 200)
        response = requests.post(self.uri_auth, data={"username":"v6@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})

    def test_DELETE_authorized_user_delete_someself(self):
        response = requests.post(self.uri_users, data={"email":"v7@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"v7@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})
        self.assertEqual(response.status_code, 204)

    def test_DELETE_superuser_delete_of_any_user(self):
        response = requests.post(self.uri_users, data={"email":"v8@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"test@test.com", "password":"password123"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})
        self.assertEqual(response.status_code, 204)

    def test_PUT_superuser_put_of_any_user(self):
        response = requests.post(self.uri_users, data={"email":"v9@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"test@test.com", "password":"password123"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.put(uri_user, headers={'Authorization':'token {}'.format(token)}, 
                    data={"email":"v9@sas.com", "password":"1", "first_name":"Djohn"})
        self.assertEqual(response.status_code, 200)
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})

    def test_PATCH_superuser_patch_of_any_user(self):
        response = requests.post(self.uri_users, data={"email":"v10@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"test@test.com", "password":"password123"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        uri_user = response.json()[0]['url']
        response = requests.patch(uri_user, headers={'Authorization':'token {}'.format(token)}, 
                    data={"email":"v10@sas.com", "password":"1", "last_name":"Broun"})
        self.assertEqual(response.status_code, 200)
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})

    def test_GET_superuser_full_info(self):
        response = requests.post(self.uri_users, data={"email":"v11@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"test@test.com", "password":"password123"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        self.assertGreater(len(response.json()), 1)
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})

    def test_GET_authorized_user_get_only_self_info(self):
        response = requests.post(self.uri_users, data={"email":"v12@sas.com", "password":"1"})
        response = requests.post(self.uri_auth, data={"username":"v12@sas.com", "password":"1"})
        token = response.json()['token']
        response = requests.get(self.uri_users, headers={'Authorization': 'token {}'.format(token)})
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['email'], "v12@sas.com")
        uri_user = response.json()[0]['url']
        response = requests.delete(uri_user, headers={'Authorization':'token {}'.format(token)})
        

class AppsTests(TestCase):
        
    def test_there_are_apps(self):
        self.assertEqual('account' not in [app for app in settings.INSTALLED_APPS if not "django" in app], False)


class UserModelTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email='a@a.com', password='1')

    def test_verbose_name_of_email_field(self):
        field_param = self.user._meta.get_field('email').verbose_name
        self.assertEquals(field_param,'email address')

    def test_unique_of_email_field(self):
        field_param = self.user._meta.get_field('email').unique
        self.assertEquals(field_param,True)

    def test_max_length_of_email_field(self):
        field_param = self.user._meta.get_field('email').max_length
        self.assertEquals(field_param,254)

    def test_verbose_name_of_id_field(self):
        field_param = self.user._meta.get_field('id').verbose_name
        self.assertEquals(field_param,'ID')

    def test_auto_created_of_id_field(self):
        field_param = self.user._meta.get_field('id').auto_created
        self.assertEquals(field_param,True)

    def test_primary_key_of_id_field(self):
        field_param = self.user._meta.get_field('id').primary_key
        self.assertEquals(field_param,True)

    def test_serialize_of_id_field(self):
        field_param = self.user._meta.get_field('id').serialize
        self.assertEquals(field_param,False)

    def test_verbose_name_of_password_field(self):
        field_param = self.user._meta.get_field('password').verbose_name
        self.assertEquals(field_param,'password')

    def test_max_length_of_password_field(self):
        field_param = self.user._meta.get_field('password').max_length
        self.assertEquals(field_param, 128)

    def test_verbose_name_of_last_login_field(self):
        field_param = self.user._meta.get_field('last_login').verbose_name
        self.assertEquals(field_param,'last login')

    def test_null_of_last_login_field(self):
        field_param = self.user._meta.get_field('last_login').null
        self.assertEquals(field_param,True)

    def test_blank_of_last_login_field(self):
        field_param = self.user._meta.get_field('last_login').blank
        self.assertEquals(field_param,True)

    def test_verbose_name_of_is_superuser_field(self):
        field_param = self.user._meta.get_field('is_superuser').verbose_name
        self.assertEquals(field_param,'superuser status')

    def test_default_of_is_superuser_field(self):
        field_param = self.user._meta.get_field('is_superuser').default
        self.assertEquals(field_param, False)

    def test_help_text_of_is_superuser_field(self):
        field_param = self.user._meta.get_field('is_superuser').help_text
        self.assertEquals(field_param, 'Designates that this user has all permissions without explicitly assigning them.')

    def test_verbose_name_of_first_name_field(self):
        field_param = self.user._meta.get_field('first_name').verbose_name
        self.assertEquals(field_param,'first name')

    def test_blank_of_first_name_field(self):
        field_param = self.user._meta.get_field('first_name').blank
        self.assertEquals(field_param, True)

    def test_max_length_of_first_name_field(self):
        field_param = self.user._meta.get_field('first_name').max_length
        self.assertEquals(field_param, 30)

    def test_verbose_name_of_last_name_field(self):
        field_param = self.user._meta.get_field('last_name').verbose_name
        self.assertEquals(field_param,'last name')

    def test_blank_of_last_name_field(self):
        field_param = self.user._meta.get_field('last_name').blank
        self.assertEquals(field_param, True)

    def test_max_length_of_last_name_field(self):
        field_param = self.user._meta.get_field('last_name').max_length
        self.assertEquals(field_param, 150)

    def test_verbose_name_of_is_staff_field(self):
        field_param = self.user._meta.get_field('is_staff').verbose_name
        self.assertEquals(field_param,'staff status')

    def test_default_of_is_staff_field(self):
        field_param = self.user._meta.get_field('is_staff').default
        self.assertEquals(field_param,False)

    def test_help_text_of_is_staff_field(self):
        field_param = self.user._meta.get_field('is_staff').help_text
        self.assertEquals(field_param,'Designates whether the user can log into this admin site.')

    def test_verbose_name_of_is_active_field(self):
        field_param = self.user._meta.get_field('is_active').verbose_name
        self.assertEquals(field_param,'active')

    def test_default_of_is_active_field(self):
        field_param = self.user._meta.get_field('is_active').default
        self.assertEquals(field_param,True)

    def test_help_text_of_is_active_field(self):
        field_param = self.user._meta.get_field('is_active').help_text
        self.assertEquals(field_param, 'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')

    def test_verbose_name_of_date_joined_field(self):
        field_param = self.user._meta.get_field('date_joined').verbose_name
        self.assertEquals(field_param,'date joined')

    def test_default_of_date_joined_field(self):
        field_param = self.user._meta.get_field('date_joined').default
        self.assertEquals(field_param, django.utils.timezone.now)

    def test_verbose_name_of_balance_field(self):
        field_param = self.user._meta.get_field('balance').verbose_name
        self.assertEquals(field_param,'balance')

    def test_default_of_balance_field(self):
        field_param = self.user._meta.get_field('balance').default
        self.assertEquals(field_param, 0)

    def test_verbose_name_of_freeze_balance_field(self):
        field_param = self.user._meta.get_field('freeze_balance').verbose_name
        self.assertEquals(field_param,'freeze balance')

    def test_default_of_freeze_balance_field(self):
        field_param = self.user._meta.get_field('freeze_balance').default
        self.assertEquals(field_param, 0)

    def test_verbose_name_of_groups_field(self):
        field_param = self.user._meta.get_field('groups').verbose_name
        self.assertEquals(field_param,'groups')

    def test_blank_of_groups_field(self):
        field_param = self.user._meta.get_field('groups').blank
        self.assertEquals(field_param, True)

    def test_help_text_of_groups_field(self):
        field_param = self.user._meta.get_field('groups').help_text
        self.assertEquals(field_param, 'The groups this user belongs to. A user will get all permissions granted to each of their groups.')

    def test_USERNAME_FIELD(self):
        self.assertEquals(self.user.USERNAME_FIELD, 'email')

    def test_REQUIRED_FIELDS(self):
        self.assertEquals(self.user.REQUIRED_FIELDS, [])

    def test_objects(self):
        self.assertEquals(isinstance(User.objects, CustomUserManager), True)

    def test___str__(self):
        self.assertEquals(self.user.__str__(), self.user.email)


class UserSerializerTests(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.hostname = socket.gethostname()
        cls.IP = socket.gethostbyname(cls.hostname)
        cls.uri_users = 'http://' + cls.IP + ':8000' + '/users/'
        cls.uri_auth = 'http://' + cls.IP + ':8000' + '/api-token-auth/'
        response = requests.post(cls.uri_users, data={"email":"v13@sas.com", "password":"1"})
        response = requests.post(cls.uri_auth, data={"username":"v13@sas.com", "password":"1"})
        cls.token = response.json()['token']
        response = requests.get(cls.uri_users, headers={'Authorization': 'token {}'.format(cls.token)})
        cls.uri_user = response.json()[0]['url']

    @classmethod
    def tearDownClass(cls):
        response = requests.delete(cls.uri_user, headers={'Authorization':'token {}'.format(cls.token)})


    def test_put_authorized_user_change_readonly_groups(self):
        response = requests.put(self.uri_user, headers={'Authorization':'token {}'.format(self.token)}, 
                    data={"email":"v13@sas.com", "password":"1", "groups":'sellers', "first_name":"Jim"})
        self.assertEqual(response.status_code, 403)


    def test_put_authorized_user_change_readonly_balance(self):
        response = requests.put(self.uri_user, headers={'Authorization':'token {}'.format(self.token)}, 
                    data={"email":"v13@sas.com", "password":"1", "balance":100, "first_name":"Jim"})
        self.assertEqual(response.status_code, 403)

    def test_put_authorized_user_change_readonly_freeze_balance(self):
        response = requests.put(self.uri_user, headers={'Authorization':'token {}'.format(self.token)}, 
                    data={"email":"v13@sas.com", "password":"1", "freeze_balance":100, "first_name":"Jim"})
        self.assertEqual(response.status_code, 403)

    def test_put_authorized_user_change_readonly_is_active(self):
        response = requests.put(self.uri_user, headers={'Authorization':'token {}'.format(self.token)}, 
                    data={"email":"v13@sas.com", "password":"1", "is_active":False, "first_name":"Jim"})
        self.assertEqual(response.status_code, 403)

    def test_put_authorized_user_change_readonly_is_staff(self):
        response = requests.put(self.uri_user, headers={'Authorization':'token {}'.format(self.token)}, 
                    data={"email":"v13@sas.com", "password":"1", "is_staff":False, "first_name":"Jim"})
        self.assertEqual(response.status_code, 403)

    def test_put_authorized_user_change_readonly_date_joined(self):
        response = requests.put(self.uri_user, headers={'Authorization':'token {}'.format(self.token)}, 
                    data={"email":"v13@sas.com", "password":"1", "date_joined":'21.12.20', "first_name":"Jim"})
        self.assertEqual(response.status_code, 403)

    def test_put_authorized_user_change_readonly_last_login(self):
        response = requests.put(self.uri_user, headers={'Authorization':'token {}'.format(self.token)}, 
                    data={"email":"v13@sas.com", "password":"1", "last_login":'21.12.20', "first_name":"Jim"})
        self.assertEqual(response.status_code, 403)

    def test_patch_authorized_user_change_readonly_groups(self):
        response = requests.patch(self.uri_user, headers={'Authorization':'token {}'.format(self.token)}, 
                    data={"email":"v13@sas.com", "password":"1", "groups":'sellers', "first_name":"Jim"})
        self.assertEqual(response.status_code, 403)


    def test_patch_authorized_user_change_readonly_balance(self):
        response = requests.patch(self.uri_user, headers={'Authorization':'token {}'.format(self.token)}, 
                    data={"email":"v13@sas.com", "password":"1", "balance":100, "first_name":"Jim"})
        self.assertEqual(response.status_code, 403)

    def test_patch_authorized_user_change_readonly_freeze_balance(self):
        response = requests.patch(self.uri_user, headers={'Authorization':'token {}'.format(self.token)}, 
                    data={"email":"v13@sas.com", "password":"1", "freeze_balance":100, "first_name":"Jim"})
        self.assertEqual(response.status_code, 403)

    def test_patch_authorized_user_change_readonly_is_active(self):
        response = requests.patch(self.uri_user, headers={'Authorization':'token {}'.format(self.token)}, 
                    data={"email":"v13@sas.com", "password":"1", "is_active":False, "first_name":"Jim"})
        self.assertEqual(response.status_code, 403)

    def test_patch_authorized_user_change_readonly_is_staff(self):
        response = requests.patch(self.uri_user, headers={'Authorization':'token {}'.format(self.token)}, 
                    data={"email":"v13@sas.com", "password":"1", "is_staff":False, "first_name":"Jim"})
        self.assertEqual(response.status_code, 403)

    def test_patch_authorized_user_change_readonly_date_joined(self):
        response = requests.patch(self.uri_user, headers={'Authorization':'token {}'.format(self.token)}, 
                    data={"email":"v13@sas.com", "password":"1", "date_joined":'21.12.20', "first_name":"Jim"})
        self.assertEqual(response.status_code, 403)

    def test_patch_authorized_user_change_readonly_last_login(self):
        response = requests.patch(self.uri_user, headers={'Authorization':'token {}'.format(self.token)}, 
                    data={"email":"v13@sas.com", "password":"1", "last_login":'21.12.20', "first_name":"Jim"})
        self.assertEqual(response.status_code, 403)
