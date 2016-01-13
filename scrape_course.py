import config
from piazza_api import Piazza


class Post(object):
    """
    A Post class to encapsulate the post data
    """
    def __init__(self, post):
        self.post_number = post['nr']
        self.author = post['history'][0]['uid']
        self.subject = post['history'][0]['subject']
        self.date = post['history'][0]['created']
        self.folders = post['folders']
        self.unique_views = post['unique_views']

        self.post_content = post['history'][-1]['content']
        self.get_answers(post)

    def get_post_content(self, post):
        return post['history'][-1]['content']

    def get_answers(self, post):
        for child in post['children']:
            if child['type'] == 'i_answer':
                self.post_instructor_answer = child['history'][-1]['content']
            if child['type'] == 's_answer':
                self.post_student_answer = child['history'][-1]['content']

    def output(self, file):
        pass
        # we might want to print results out to file


def main():
    username = config.username
    password = config.password
    class_id = 'idj5lp6gixc6xn'
    p = Piazza()
    p.user_login(email=username, password=password)
    cis121 = p.network(class_id)

    #limit to 10 for now
    posts = cis121.iter_all_posts(limit=10)
    post_obj = [Post(post) for post in posts]
    print post_obj


if __name__ == "__main__":
    main()