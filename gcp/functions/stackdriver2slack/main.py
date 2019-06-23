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
    import pprint
    pprint.pprint(incident)

    if incident['state'] == 'open':
        attachments = [{
            'pretext': incident['summary'],
            'author_name': incident['incident_id'],
            'title': incident['policy_name'],
            'title_link': incident['url'],
            'text': incident['documentation']['content'],
            'color': '#ff0000',
            'footer': incident['state'],
            'ts': incident['started_at'],
        }]

    elif incident['state'] == 'closed':
        attachments = [{
            'author_name': incident['incident_id'],
            'title': incident['policy_name'],
            'title_link': incident['url'],
            'color': '#36a64f',
            'footer': incident['state'],
            'ts': incident['ended_at'],
        }]

    else:
        raise Exception('unknown incident state: {}'.format(incident['state']))

    slack.notify(attachments=attachments)
