
from flask import Blueprint
from flask import render_template, request
from models import MESSAGES

hello = Blueprint('hello', __name__)


@hello.route('/')
@hello.route('/hello')
@hello.route('/hello/<user>')
def hello_world(user=None):
    #print user
    user = request.args.get('userg','Jose')
    return render_template('index.html', user=user)


#    return MESSAGES['default']
# @app.route('/')
# @app.route('/hello')
# def hello_world():
#     return MESSAGES['default']


# @app.route('/show/<key>')
# def get_message(key):
#     return MESSAGES.get(key) or "%s not found!" % key
#
#
# @app.route('/add/<key>/<message>')
# def add_or_update_message(key, message):
#     MESSAGES[key] = message
#     return "%s Added/Updated" % key
