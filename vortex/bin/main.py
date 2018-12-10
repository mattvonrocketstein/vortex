# -*- coding: utf-8 -*-
""" vortex.bin.main
    A command-line-interface that demos/exercises most of the features available
"""

from pprint import pprint
import click
from vortex.logger import LOGGER


@click.group(invoke_without_command=True)
@click.option('--serve', help='run slash-command server', default=False, is_flag=True)
@click.option('--mirror', help='run the link-mirroring process', default=False, is_flag=True)
@click.option('--topic', help='set reddit topic name', default='general')
@click.option('--channel', help='set slack channel name', default='general')
@click.option('--describe-topics', help='describe all topics in reddit', default=False, is_flag=True)
@click.option('--dump-topic', help='dump contents of reddit topic', default=False, is_flag=True)
@click.option('--describe-channels', help='describe all channels in slack', default=False, is_flag=True)
@click.option('--describe-links', help='describe links in slack channel (used with --channel)', default=False, is_flag=True)
@click.option('--search', help='search links under given topic (used with --topic)')
@click.pass_context
def entry(ctx, serve, mirror, topic, channel, dump_topic, describe_topics, describe_links, describe_channels, search, ):
    if serve:
        LOGGER.debug("dispatching for serve")
        from vortex.app import APP
        result = APP.run(debug=True)
    elif mirror:
        LOGGER.debug("dispatching for mirror")
        from vortex.cron import mirror_links
        result = mirror_links()
    elif describe_channels:
        LOGGER.debug("dispatching for describe-channels")
        from slacks import slacks
        result = slacks().channels
    elif describe_links:
        err = '--channel must be provided with --describe-links'
        assert channel, err
        LOGGER.debug("dispatching for describe-links")
        from vortex.slack import Slack
        result = Slack()[channel]
        result = result.links
    elif describe_topics:
        LOGGER.debug("dispatching for describe-topics")
        from redditdb import RedditDB
        result = [x for x in RedditDB()]
    elif dump_topic:
        err = '--topic must be provided with --dump-topic'
        assert topic, err
        LOGGER.debug("dispatching for dump-topic")
        from redditdb import RedditDB
        topic = RedditDB()[topic]
        LOGGER.debug("got topic: {}".format(topic))
        result = [x for x in topic]
    elif search:
        err = '--topic must be provided with --search'
        assert topic, err
        LOGGER.debug("dispatching for search")
        from vortex.reddit import Reddit
        result = Reddit()[topic].search(search)
    pprint(result)
    return result
