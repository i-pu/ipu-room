from flask_httpauth import HTTPBasicAuth
import slackweb

auth = HTTPBasicAuth()

users = {
    "john": "hello",
    "susan": "bye"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@auth.login_required
def entry_point(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    # https://hooks.slack.com/services/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
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        print(type(request), flush=True)
        slack = slackweb.Slack(url='https://hooks.slack.com/services/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')
        slack.notify(text='hello, auth: {}'.format(auth.username()))
