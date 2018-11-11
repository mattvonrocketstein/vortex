""" vortex.app
"""
from flask import Flask
from vortex.logger import LOGGER
from vortex.slack import Slack
from vortex.reddit import Reddit
APP = app = Flask(__name__)
SLACK = Slack()
REDDIT = Reddit()


@app.route('/vortex/link-history', methods=['GET', 'POST'])
def link_history_handler():
    """ """
    now = str(datetime.datetime.now())
    args = request.form.get('text')
    command = request.form.get('command')
    channel_id = request.form.get('channel_id')
    channel = SLACK.cbi.get(channel_id)
    status_msg = ('processing command `{}` originating '
                  "in channel `{}` with args `{}` at `{}`")
    status_msg = status_msg.format(command, channel, args, now)
    if not channel:
        # probably a direct message or a non-whitelisted channel
        error_msg = (
            "Cannot generate attachments without "
            "a (whitelisted) channel context")
        attachments = [dict(text=error_msg,)]
    else:
        attachments = REDDIT[channel].attachments
    return jsonify(dict(text=status_msg, attachments=attachments))


def mirror_links():
    """
    mirrors links from slack to reddit.
    this entrypoint is scheduled by lambda
    """
    REDDIT.mirror_recent_attachments()
