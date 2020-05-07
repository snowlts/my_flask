import unittest
from selenium import webdriver
from app import create_app,db,fake
from app.models import Role,User
from threading import Thread
import re
from time import sleep
import selenium.webdriver.support.ui as ui



class SeleniumTestCase(unittest.TestCase):
    client=None

    @classmethod
    def setUpClass(cls):
        #start chrome
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_argument('headless')
        try:
            cls.client = webdriver.Chrome(r"D:\Program Files\Python\Python37-32\chromedriver.exe",chrome_options=options)
        except:
            print('client not started')

        #skip these tests if chrome could not be started
        if cls.client:
            #create the application
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            #suppress logging to keep unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel('ERROR')

            #create the database and populate with some fake data
            db.create_all()
            Role.insert_roles()
            fake.users(10)
            fake.posts(10)

            #add in administrator user
            r_admin = Role.query.filter_by(name='Administrator').first()
            u = User(email='john@example.com',
                     username='john',password='cat',
                     confirmed=True,role=r_admin)
            db.session.add(u)
            db.session.commit()

            #start the flask server in thread
            cls.server_thr = Thread(target=cls.app.run,
                         kwargs={'debug':False})
            cls.server_thr.start()
            # print('alive?',cls.server_thr.is_alive())

            #give the server a second to ensure it is up
            sleep(2)
            # print('alive?',cls.server_thr.is_alive())


    @classmethod
    def tearDownClass(cls) -> None:
        if cls.client:
            #stop the Flask server and the browser
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.quit()
            cls.server_thr.join()


            #destroy database
            db.drop_all()
            db.session.remove()

            #remove the app context
            cls.app_context.pop()

    def setUp(self) -> None:
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self) -> None:
        pass


    def test_admin_home_page(self):
        #navigate to home page
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Hello,\s+Stranger\s+!',self.client.page_source))


        #navigate to login page
        self.client.find_element_by_link_text('Log In').click()
        self.assertTrue('<h1>Login</h1>' in self.client.page_source)


        #login
        self.client.find_element_by_name('email').send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('Hello,\s+john\s+!',self.client.page_source))

        #navigate to user's profile page
        print(self.client.page_source)
        # wait = ui.WebDriverWait(self.client, 10)
        # wait.until(lambda driver: self.client.find_element_by_link_text('john'))
        self.client.find_element_by_link_text('john').click()
        self.client.find_element_by_link_text('User Profile').click()
        self.assertIn('<h1>john</h1>',self.client.page_source)




