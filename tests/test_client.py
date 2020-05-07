import unittest
from app import create_app,db
from app.models import User,Role
import re


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertTrue('Stranger' in response.get_data(as_text=True))

    def test_register_and_login(self):
        #获取注册页面
        # register_page = self.client.get('/auth/register')
        # self.assertEqual(register_page.status_code,200)
        # self.assertTrue('Register' in register_page.get_data(as_text=True))

        #注册
        # user = User.query.filter_by(email='john@example.com').first()
        # print(user)
        response = self.client.post('/auth/register',data={
            'email':'john@example.com',
            'username':'john',
            'password':'cat',
            'password2':'cat'
        })
        # user = User.query.filter_by(email='john@example.com').first()
        # print(user)
        # print(response.status_code,response.get_data())
        self.assertEqual(response.status_code,302)

        #登录(邮箱未确认）
        response = self.client.post('/auth/login',data={
            'email':'john@example.com',
            'password': 'cat'},follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertTrue(re.search('Hello,\s+john!',response.get_data(as_text=True)))
        self.assertTrue('You have not confirmed your account yet!' in response.get_data(as_text=True))

        #确认邮箱
        user = User.query.filter_by(email = 'john@example.com').first()
        # print(user)
        token = user.generate_confirmation_token()
        response = self.client.get('/auth/confirm/{}'.format(token),follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertTrue('You have confirmed your account' in response.get_data(as_text=True))

        #登出
        response = self.client.get('/auth/logout',follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertTrue('You have been logged out' in response.get_data(as_text=True))



