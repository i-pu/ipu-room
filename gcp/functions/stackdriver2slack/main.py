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
        content = ('incident_id: {}, resource: {}\n'
                   'policy: {}, condition: {}\n'
                   '{}\n'
                   'summary: {}\n'
                   ).format(incident['incident_id'],
                            incident['resource'],
                            incident['policy_name'],
                            incident['condition_name'],
                            incident['documentation']['content'],
                            incident['summary'])
        slack.api_call(
            "files.upload",
            content=content,
            title='error happen!'
        )

    elif incident['state'] == 'closed':
        text = 'closed: incident_id: {}'.format(incident['incident_id'])
        slack.notify(text=text, mrkdwn=True)

    else:
        raise Exception('unknown incident state: {}'.format(incident['state']))
