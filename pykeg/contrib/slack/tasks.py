# Copyright 2014 Bevbot LLC, All Rights Reserved
#
# This file is part of the Pykeg package of the Kegbot project.
# For more information on Pykeg or Kegbot, see http://kegbot.org/
#
# Pykeg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Pykeg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pykeg.  If not, see <http://www.gnu.org/licenses/>.

"""Celery tasks for Slack plugin."""

from pykeg.celery import app
from pykeg.plugin import util
from pykeg.core.util import get_version
from kegbot.util import kbjson

from slacker import Slacker

logger = util.get_logger(__name__)


@app.task(name='slack_post', expires=180)
def slack_post(slack_conf, msg, image_file=''):
    """Posts an event to slack.

    """
    logger.info('Posting to slack: msg=%s image_file=%s' % (msg, image_file))

    slack = Slacker(slack_conf['token'])
    if image_file:
        slack.files.upload(image_file, channels=slack_conf['channel_id'], initial_comment=msg)
    else:
        slack.chat.post_message(slack_conf['channel'], msg, slack_conf['botname'])


