import unittest
from app.models import Post

class PostTest(unittest.TestCase):
        '''
        Test class to test the behavior of the Post class
        '''

        def setUp(self):
            '''
            Set up method that will run before every Test
            '''
            self.new_post = Post(1 ,'New','New','New','New',0,'New','New')

        def test_instance(self):
            '''
            '''
            self.assertTrue(isinstance(self.new_post, Post))

        def test_to_check_instance_variables(self):
            '''
            '''
            self.assertEquals(self.new_post.id, 1)
            self.assertEquals(self.new_post.title, 'New')
            self.assertEquals(self.new_post.description, 'New')
            self.assertEquals(self.new_post.comments, 'New')
            self.assertEquals(self.new_post.stars, 0)
            self.assertEquals(self.new_post.posted_p, 'New')
            self.assertEquals(self.new_post.user_p, 'New')




if __name__ == '__main__':
    unittest.main()