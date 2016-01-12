import unittest
import config
from piazza_api import Piazza

from scrape_course import Post


class TestPost(unittest.TestCase):
    # def setUp(self):
    #     username = config.username
    #     password = config.password
    #     class_id = 'idj5lp6gixc6xn'
    #     p = Piazza()
    #     p.user_login(email=username, password=password)
    #     self.cis121 = p.network(class_id)
    #

    def test_simple_post(self):
        username = config.username
        password = config.password
        class_id = 'idj5lp6gixc6xn'
        p = Piazza()
        p.user_login(email=username, password=password)
        self.cis121 = p.network(class_id)
        post_json = self.cis121.get_post(1873)
        p = Post(post_json)
        self.assertEqual(p.subject, u'Neighbors function for our own digraph class in milestone 0')
        self.assertEqual(p.unique_views, 48)
        self.assertEqual(p.post_instructor_answer,
                         u'''<p>The neighbors function is already implemented for you in the ImmutableSimpleGraph interface, so you don&#39;t need to worry about it. (I believe it just does outNeighbors)</p>''')

