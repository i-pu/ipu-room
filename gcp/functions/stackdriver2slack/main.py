import os

from flask_httpauth import HTTPBasicAuth
import slackweb

auth = HTTPBasicAuth()

users = {
    os.getenv('BASICAUTH_USERNAME'): os.getenv('BASICAUTH_PASSWORD'),
}
slack_channel = os.getenv('SLACK_CHANNEL')

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@auth.login_required
def entry_point(request):

    request_json = request.get_json()

    if request.args and 'message' in request.args:
        return request.args.get('message')

    elif request_json and 'message' in request_json:
        return request_json['message']

    else:
        slack = slackweb.Slack(url=slack_channel)
        slack.notify(text='hello, auth: {}'.format(auth.username()))
