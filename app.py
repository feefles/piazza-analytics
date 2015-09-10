from flask import Flask
import config
from piazza_api import Piazza
import json

app = Flask(__name__)

username = config.username
password = config.password

@app.route('/')
def index():
    return "hello world"



from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/tag_good/<int:post_id>')
@crossdomain(origin='*')
def get_person(post_id):
    p = Piazza()
    p.user_login(email=username, password=password)
    cis121 = p.network("idj5lp6gixc6xn")

    post = cis121.get_post(post_id)
        # print post
    d = {
        "tag_good": [], 
        "tag_endorse": []
    }
    if 'tag_good' in post:
        for person in post['tag_good']:
            d['tag_good'].append(person['name'])
    if 'tag_endorse' in post:
        for person in post['tag_endorse']:
            d['tag_endorse'].append(person['name'])
    return json.dumps(d)


if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
