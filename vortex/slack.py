""" vortex.slack
    Customization of the slack client for vortex-specific usage
"""
import os
from pprint import pprint
from memoized_property import memoized_property
from slacks import slacks


class SlackChannel(slacks):

    def __init__(self, name=None, id=None, slack=None, **kargs):
        super(SlackChannel, self).__init__(**kargs)
        self.slack = None
        self.name = name
        self.id = id

    def __repr__(self):
        return '<SlackChannel: name={} id={}>'.format(self.name, self.id)

    __str__ = __repr__

    @memoized_property
    def links(self):
        result = self.get_link_history()
        return [x.get('original_url') for x in result]

    def send(self, chan_id=None, msg="default message", attachments=[]):
        """ """
        result = self.bot_client.api_call(
            "chat.postMessage",
            channel=self.id,
            attachments=attachments,
            text=msg)
        self.logger.debug(pprint.pformat(result))
        return result

    def get_link_history(self):
        response = self.user_client.api_call(
            "channels.history",
            channel=self.id, count=1000)
        if 'messages' not in response:
            self.logger.warning(pprint.pformat(response))
            raise ValueError('response does not contain messages')
        out = []
        for msg in response['messages']:
            out += msg.get('attachments', [])
        return out


class Slack(slacks):
    """
    Handle on Slack.  This behaves like a dictionary where both
    SLACK[chan_name] and SLACK[chan_id] return a SlackChannel object
    """
    @memoized_property
    def channel_whitelist(self):
        if 'SLACK_CHANNEL_WHITELIST' in os.environ:
            result = os.environ['SLACK_CHANNEL_WHITELIST'].split(',')
        else:
            result = [c['name'] for c in self._CHANNELS]
        self.logger.debug("channel whitelist: {}".format(result))
        return result

    @memoized_property
    def _CHANNELS(self):
        self.debug('loading channels')
        response = self.user_client.api_call("channels.list", count=1000)
        if 'channels' not in response:
            self.logger.warning(pprint.pformat(response))
            raise ValueError('error getting channel list')
        return response['channels']

    @memoized_property
    def cbn(self):
        """ channels by name mapping """
        return dict([[c['name'], c['id']]
                     for c in self._CHANNELS if c['name'] in self.channel_whitelist])

    @memoized_property
    def cbi(self):
        """ channels by id mapping """
        return dict([[c['id'], c['name']]
                     for c in self._CHANNELS if c['name'] in self.channel_whitelist])

    def __getitem__(self, name_or_id):
        if name_or_id not in self.cbn and name_or_id not in self.cbi:
            err = "no such channel `{}`, or channel is not whitelisted"
            raise KeyError(err.format(name_or_id))
        name = name_or_id if name_or_id in self.cbn else self.cbi[name_or_id]
        _id = name_or_id if name_or_id in self.cbi else self.cbn[name_or_id]
        return SlackChannel(name=name, id=_id, slack=self)

    def __iter__(self):
        return iter(self.cbi)

    def get_link_history(self):
        """ returns a dictionary of
            { chan_id:[..slack attachment objects..] }
            when chan_id is not provided, the results will include all channels
        """
        return dict([[chan_id, self[chan_id].get_link_history()] for chan_id in self])
