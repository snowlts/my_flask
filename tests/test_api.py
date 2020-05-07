import unittest
from app import create_app,db
from app.models import Role,User,Post
from base64 import b64encode
from flask import url_for,json



class APITestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self,username,password):
        return {
            'Authorization':
                'Basic '+ b64encode((username+':'+password).encode('utf-8')).decode('utf-8'),
            'Accept':'application/json',
            'Content-Type':'application/json'
        }

    def test_no_auth(self):
        response = self.client.get('/api/v1/posts/',content_type='application/json')
        self.assertEqual(response.status_code,401)

    def test_posts(self):
        #add a new user
        role = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(role)
        user = User(email='john@example.com',username='john',password='cat',role=role,confirmed=True)
        db.session.add(user)
        db.session.commit()

        #write a post
        response = self.client.post('/api/v1/posts/',
                                    headers=self.get_api_headers(user.email,'cat'),
                                    data=json.dumps({'body': 'body of the *blog* post'}))
        self.assertEqual(response.status_code,201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        #get the new post
        response = self.client.get(url,
                                   headers=self.get_api_headers(user.email,'cat'))
        self.assertEqual(response.status_code,200)
        json_response = json.loads(response.get_data(as_text=True))
        print(json_response['url'])
        self.assertEqual('http://localhost'+json_response['url'],url)
        self.assertEqual(json_response['body'],'body of the *blog* post')
        self.assertEqual(json_response['body_html'],'<p>body of the <em>blog</em> post</p>')


