import unittest
from app.models import Email
from app import db

class EmailTest(unittest.TestCase):
    '''
    Test class to test the behavior of the Email class
    '''
    def setUp(self):
        '''
        Set up method that will run before every test
        '''
        self.new_email = Email(name='Keller', email_data='abc@example.com')

    def tearDown(self):
        '''
        Method that will clear up after test has run
        '''
        db.session.delete(self.new_email)
        db.session.commit()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_email,Email))

    def test_check_instance_variables(self):
        self.assertEquals(self.new_email.name,'Keller')
        self.assertEquals(self.new_email.email_data,'abc@example.com')


    def test_save_review(self):
        self.new_email.save_email()
        self.assertTrue(len(Email.query.all())>0)
