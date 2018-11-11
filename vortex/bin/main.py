""" vortex.bin.main
"""

import click
from .app import APP


def entry():
    """
    We only need this for local development,
    the lambda deployments specify their own entry points
    """
    APP.run(debug=True)
