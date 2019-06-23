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
    for i in request_json.items():
        print(i, flush=True)
    slack = slackweb.Slack(url=slack_channel)
    slack.notify(text='hello, auth: {}'.format(auth.username()))
