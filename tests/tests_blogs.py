import unittest
from app.models import Blog
from app import db
from datetime import datetime


class CommentTest(unittest.TestCase):

    def setUp(self):
        self.new_blog = Blog(title='New Blog',blog_content='This is the content', date_posted=datetime.now())

    def tearDown(self):
        db.session.delete(self.new_blog)
        db.session.commit()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog,Blog))

    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog.title,'New Blog')
        self.assertEquals(self.new_blog.blog_content,'This is the content')
        self.assertEquals(self.new_blog.date_posted,datetime.now())

    def test_save_blog(self):
        self.new_blog.save_blog()
        self.assertTrue(len(Blog.query.all())>0)
