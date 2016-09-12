import json
from HTMLParser import HTMLParser

import config

html_parser = HTMLParser()
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
        self.post_instructor_answer = ""
        self.post_student_answer = ""
        self.get_answers(post)
        self.outlinks = []
        self.inlinks = []

    def get_post_content(self, post):
        return post['history'][-1]['content']

    def get_answers(self, post):
        for child in post['children']:
            if child['type'] == 'i_answer':
                self.post_instructor_answer = child['history'][0]['content']
            if child['type'] == 's_answer':
                self.post_student_answer = child['history'][0]['content']

    def output(self, file):
        pass
        # we might want to print results out to file

    def parse_outlinks(self):
        for token in self.post_instructor_answer.split():
            token_unescaped = html_parser.unescape(token)
            if '@' in token_unescaped:
                link_number = ''.join([str(s) for s in str(token_unescaped) if s.isdigit()])
                if link_number == '':
                    continue
                self.outlinks.append(link_number)
                # for debugging before we make the whole graph
                if link_number in all_posts:
                    all_posts[link_number].inlinks.append(self.post_number)



all_posts = {}
def main():
    current_data = {}
    try: 
        with open(config.LOCAL_DATA_FILE_NAME, 'r') as data_file:
            try:
                current_data = json.load(data_file)
            except ValueError: # empty file
                current_data = {}
    except IOError: #file didn't exist
        # current_data = {}
        print "IOError!"
    for key, value in current_data.iteritems():
        if value['status'] == 'deleted':
            continue
        post_obj = Post(value)
        all_posts[key] = post_obj
    for post_number, post in all_posts.iteritems():
        post.parse_outlinks()
    return all_posts



if __name__ == "__main__":
    main()