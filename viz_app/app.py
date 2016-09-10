import os

import flask
from flask import render_template

from viz_app import scrape_course

app = flask.Flask(__name__)


@app.route('/')
def index():
    return '17'

@app.route('/graph', methods=['GET'])
def returnGraphData():
    graph = scrape_course.main()
    nodes = [{'data': {'id': id, 'postContent': post.post_content}} for (id, post) in graph.iteritems() if len(post.outlinks + post.inlinks) != 0]
    edges = [{'data': {'source': str(post.post_number), 'target': outlink}} for post in graph.values() for outlink in post.outlinks]
    return render_template('index.html', nodes=nodes, edges=edges)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)