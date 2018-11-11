# -*- coding: utf-8 -*-
""" vortex.bin.main
"""

import click
from vortex.app import APP
from vortex.logger import LOGGER


@click.group(invoke_without_command=True)
@click.option('--serve', help='run slash-command server', default=False, is_flag=True)
# @click.argument('keyname', nargs=1)
# @click.argument('command', nargs=-1)
@click.pass_context
def entry(ctx, serve):
    # ctx.obj = dict(dry_run=dry_run)
    if serve:
        APP.run(debug=True)
