""" vortex.reddit
"""


class Reddit(RedditBase):
    def __init__(self, **kargs):
        super(Reddit, self).__init__(**kargs)
        # prime the cache just so logging isn't weird
        self.channels

    def __getitem__(self, submission_name):
        result = self.channels[self.normalize_channel_name(submission_name)]
        return ChannelMirror(result)

    def mirror_recent_attachments(self, target_chan_id=None):
        """
        compute recent attachments in slack, then attempts
        to synchronize each one to subreddit. sync is NOOP
        if link is already present.
        """
        for chan_id, slack_attachments in SLACK.get_link_history().items():
            if target_chan_id and chan_id != target_chan_id:
                continue
            chan_name = SLACK.cbi[chan_id]
            msg = 'synchronizing links from: {}'.format(chan_name)
            self.debug(msg, divider=True)
            SLACK['robots'].send(msg=msg)
            for attachment in slack_attachments:
                self.sync_attachment(chan_name, attachment)

    def sync_attachment(self, chan_name, slack_attachment):
        """ synchronizes a attachment from slack to reddit """
        original_url = slack_attachment.get('original_url')
        if not original_url:
            # NOOP: whatever this attachment is, it doesnt have a URL
            return
        reddit_attachments = self[chan_name].attachments
        if original_url in reddit_attachments:
            # NOOP: already a comment representing this attachment
            self.debug("skipping: {}".format(original_url))
        else:
            # looks new, persist the data
            self.debug('synch: chan={} url={}'.format(
                chan_name, original_url))
            self[chan_name].reply(original_url + '\n' +
                                  json.dumps(slack_attachment))

    def normalize_channel_name(self, name):
        return name.replace('#', '')

    def create_channel(self, chan_name):
        msg = 'sticky-post "{}" is missing from subreddit, will be created'
        self.debug(msg.format(chan_name))
        name = self.normalize_channel_name(chan_name)
        return self.create_toplevel_submission(
            name='#{}'.format(name),
            body='Links harvested from #{} channel'.format(name),
            send_replies=False, distinguish=True, sticky=True)

    @memoized_property
    def channels(self):
        """
        return the submissions for this subreddit
        that correspond to known slack channels
        """
        msg = 'loading (or creating) top-level reddit sticky-post structures'
        self.debug(msg)
        result = {}
        for submission_obj in self.toplevel:
            title = self.normalize_channel_name(submission_obj.title)
            if title in SLACK.cbn:
                result[title] = submission_obj
        for name in sorted(SLACK.cbn.keys()):
            if name not in result:
                result[name] = self.create_channel(name)
            else:
                self.debug('{} already present in subreddit'.format(name))
        return result
