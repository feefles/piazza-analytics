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

