import datetime
import flask
import functools
import os
import piazza_api
import subprocess
import StringIO

app = flask.Flask(__name__)

import config

USERNAME = config.username
PASSWORD = config.password


@app.route('/')
def index():
    return '17'


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, datetime.timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = flask.current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and flask.request.method == 'OPTIONS':
                resp = flask.current_app.make_default_options_response()
            else:
                resp = flask.make_response(f(*args, **kwargs))
            if not attach_to_all and flask.request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return functools.update_wrapper(wrapped_function, f)
    return decorator


@app.route('/tag_good/<class_id>/<int:post_id>')
@crossdomain(origin='*')
def get_person(class_id, post_id):
    p = piazza_api.Piazza()
    p.user_login(email=USERNAME, password=PASSWORD)
    cis121 = p.network(class_id)

    post = cis121.get_post(post_id)
        # print post
    d = {
        'tag_good': [],
        'tag_endorse_student': [],
        'tag_endorse_instructor': []
    }
    if 'tag_good' in post:
        for person in post['tag_good']:
            d['tag_good'].append(person['name'])
    for child in post['children']:
        if 'tag_endorse' in child and 'type' in child:
            # this is an instructor post
            if child['type'] == 'i_answer':
                for person in child['tag_endorse']:
                    d['tag_endorse_instructor'].append(person['name'])
            elif child['type'] == 's_answer' : # this is a student answer
                for person in child['tag_endorse']:
                    d['tag_endorse_student'].append(person['name'])
    return flask.json.dumps(d)


###############################################################################
# TODO: This slack stuff shouldn't be in the same app
###############################################################################

def _init_piazza():
    p = piazza_api.Piazza()
    p.user_login(email=USERNAME, password=PASSWORD)
    return p


# FIXME: This Piazza object might need to be refreshed if the cookies expire
PIAZZA = _init_piazza()

EXPECTED_SLACK_TOKEN = config.slack_token


def slack_POST(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        if EXPECTED_SLACK_TOKEN == flask.request.form['token']:
            return f(*args, **kwargs)
        abort(403)


def convert_html_to_markdown(text):
    p = subprocess.Popen(['pandoc', '-f', 'html', '-t', 'markdown'],
                         stdin=subprocess.PIPE)
    # ugh python text encoding problems
    output = p.communicate(text.encode('utf-8'))
    return output


def convert_post_to_slack_message(post, clazz, class_id):
    latest = post['history'][0]
    user = clazz.get_users(['hqfm21ju8ek3vo'])[0]
    content = convert_html_to_markdown(latest['content'])
    slack_attachment = {
        'fallback': 'Piazza post @{}'.format(post['nr']),
        'pretext': 'Piazza post @{}'.format(post['nr']),
        'author_name': user['name'] + (' (anonymous)' if latest['anon'] == 'stud' else ''),
        # how do we convert get the actual image given by user['photo']
        # 'author_icon': user['photo'],
        'title': latest['subject'],
        'title_link': 'https://www.piazza.com/{}?cid={}'.format(class_id, post['nr']),
        'text': content,
        'fields': [{'title': 'created', 'value': latest['created'], 'short': True},
                   {'title': 'views', 'value': post['unique_views'], 'short': True},
                   {'title': 'tags', 'value': ', '.join(post['folders']) if post['folders'] else '(none)', 'short': False}
        ]
    }
    return flask.jsonify(attachments=[slack_attachment])


@app.route('/slack/<class_id>', methods=['POST'])
def get_post_for_slack(class_id):
    clazz = PIAZZA.network(class_id)
    post_id = flask.request.form['text']
    post = clazz.get_post(post_id)
    return convert_post_to_slack_message(post, clazz, class_id)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)
