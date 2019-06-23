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
    incident = request_json['incident']
    slack = slackweb.Slack(url=slack_channel)
    if incident['state'] == 'open':
        text = ('error happen!\n',
                'incident_id: {}, resource: {}\n'.format(
                    incident['incident_id'],
                    incident['resource']
                ),
                'policy: {}, condition: {}\n'.format(
                    incident['policy_name'],
                    incident['condition_name'],
                ),
                '{}\n'.format(incident['document']['content']),
                'summary: {}\n'.format(incident['summary']),
                )
    elif incident['state'] == 'closed':
        text = (
            'closed: incident_id: {}'.format(incident['incident_id'])
        )
    slack.notify(text=text, mrkdwn=True)
