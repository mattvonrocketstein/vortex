""" vortex.cron
"""
from vortex.reddit import Reddit


def mirror_links():
    """
    mirrors links from slack to reddit.
    this entrypoint is scheduled by lambda
    """
    Reddit().mirror_recent_attachments()
