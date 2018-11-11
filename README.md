<table>
  <tr><th><strong>stack-core</strong></th>
    <th style="padding:0px 5px;text-align:right;float:right;">
      <small><small>
      <a href=#overview>Overview</a> |
      <a href=#design>Design</a> |
      <a href=#prerequisites>Prerequisites</a> |
      <a href=#usage>Usage</a> |
      <a href=#running-tests>Running Tests</a> |
      <a href=#related-work>Related Work</a>
      </small><small>
    </th>
  </tr>
  <tr>
    <td width=15%><img src=img/icon.png style="width:150px"></td>
    <td>
    </td>
  </tr>
</table>

## Overview

This code is an experiment with various aspects of AWS lambda, featuring periodic tasks and usage of API Gateway, managed via the [zappa framework](https://github.com/Miserlou/Zappa).  It also demonstrates lambda/slack integration and lambda/reddit integration, building a bridge between slack and reddit.

Specifically, this experiment uses a subreddit as a persistent storage layer, backing up all links from whitelisted slack channels.  Why?  Besides just needing a use-case to experiment with, free slack has limits on history, and I'm tired of losing the curated contents of communal #music channels :)

## Design

1. Scheduled Execution invokes `vortex.mirror_links` function.  See also the [aws docs for building cron expressions]( https://docs.aws.amazon.com/systems-manager/latest/userguide/reference-cron-and-rate-expressions.html
) to change the schedule.  See the [Usage section](#usage) for manual invocation of the scheduled tasks.

## Prerequisites

#### Reddit User

You need at least a registered script client id/secret from reddit.  See also the documentation provided by praw library [here](https://praw.readthedocs.io/en/latest/getting_started/authentication.html#script-application).  You could set this script client id/secret up so that they are attached to your personal reddit user, but you probably just want a dedicated robot user.

#### Reddit Subreddit  

You also need a subreddit already setup for the data backend, probably one that is private and dedicated to this whole thing.  Posts that do not use the storage-backend data format can be ignored, but this is even more ridiculously inefficient because they have to be parsed first to determine that they should be ignored.

The reddit user you setup in the last step should also be a moderator for this subreddit.  (This is because sticky-thread features are used to control top-level post sorting)

#### Local Dotfiles

It's optional to do things this way, but you may want to manage configuration details outside of your code.  This library supports dot-env files natively via the [pydotenv library](#).  If the library is used from a working directory that includes a `.env` the contents will automatically loaded into `os.environ` on your behalf.  

All of the expected/supported environment variables are included below

```
# yes, we need both a bot token and a user token.
SLACK_BOT_TOKEN=xoxb-example
SLACK_USER_TOKEN=xoxp-example

REDDIT_USER=myuser
REDDIT_PASSWORD=mypassword
REDDIT_CLIENT_ID=myid
REDDIT_CLIENT_SECRET=mysecret
REDDIT_SUBREDDIT=example
```

#### Installation

For local development, these instructions assume the usage of [virtualenv wrapper](#).  You can ignore that if you prefer to do this manually, use [pip env](#) etc.  Even if you're not interested in local development, planning to use live stuff (even in a dev environment) on lambda, [zappa](#) does assume that a local virtualenv is being used.

```
$ mkvirtualenv vortex
$ workon vortex
$ pip install .
````

## Usage

```
# deploy
$ zappa deploy vortex

# update
$ zappa update vortex

# invoke
$ zappa invoke vortex.mirror_links
```

#### Running Tests

Placeholder

## Related Work

Placeholder
