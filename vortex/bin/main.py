# -*- coding: utf-8 -*-
""" vortex.bin.main

A command-line-interface that demos/exercises most of the features available
"""

import click
from vortex.logger import LOGGER


@click.group(invoke_without_command=True)
@click.option('--serve', help='run slash-command server', default=False, is_flag=True)
@click.option('--mirror', help='run the link-mirroring process', default=False, is_flag=True)
@click.option('--topic', help='set reddit topic name', default='general')
@click.option('--channel', help='set slack channel name', default='general')
@click.option('--describe-topics', help='describe all topics in reddit', default=False, is_flag=True)
@click.option('--describe-channels', help='set slack channel name', default='general')
@click.option('--describe-links', help='describe links in slack channel (used with --channel)', default='general')
@click.option('--search', help='search links under given topic (used with --topic)')
@click.pass_context
def entry(ctx, serve, mirror, topic, channel, describe_topics, describe_links, describe_channels, search, ):
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
        from vortex.slack import Slack
        result = Slack().channels
    elif describe_links:
        err = '--channel must be provided with --describe-links'
        assert channel, err
        LOGGER.debug("dispatching for describe-links")
        from vortex.slack import Slack
        result = Slack()[channel].links
    elif describe_topics:
        LOGGER.debug("dispatching for describe-topics")
        from vortex.reddit import Reddit
        result = Reddit().topics
    elif search:
        err = '--topic must be provided with --search'
        assert topic, err
        LOGGER.debug("dispatching for search")
        from vortex.reddit import Reddit
        result = Reddit()[topic_name].search(search)
    print result
    return result
