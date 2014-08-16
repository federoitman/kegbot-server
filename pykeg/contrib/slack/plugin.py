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

"""Webhook plugin for Kegbot."""

from pykeg.core.util import SuppressTaskErrors
from pykeg.plugin import plugin
from pykeg.proto import protolib

from . import forms
from . import tasks
from . import views

KEY_SITE_SETTINGS = 'settings'


class SlackPlugin(plugin.Plugin):
    NAME = 'Slack Hooks'
    SHORT_NAME = 'slack'
    DESCRIPTION = 'Posts events to slack channel'
    URL = 'http://kegbot.org'
    VERSION = '1.0.0'

    def get_admin_settings_view(self):
        return views.admin_settings

    def handle_new_events(self, events):
        for event in events:
            self.handle_event(event)

    def handle_event(self, event):
        self.logger.info('Handling new event: %s' % event.id)
        settings = self.get_site_settings()
        url = self.generate_slack_msg()
        event_dict = protolib.ToDict(event, full=True)
	msg = self.generate_slack_msg(settings, event_dict)
	if 'image' in event_dict:
            image_file = self.get_image_file(event_dict['image']['url'])

        if post:
            with SuppressTaskErrors(self.logger):
                tasks.slack_post.delay(url, post)

    ### -specific methods
    def get_image_file(self, image_url):
        # Here we would look for the image path on disk
        pass

    def generate_slack_msg(self, settings, event_dict):
        event = event_dict['kind']
	msg_template = settings.get(event+'_msg', '')
	if msg_template == '':
            return
        msg = self.replace_variables(msg_template, event_dict)

        print msg

    def replace_variables(self, msg, event_dict):
        variables = self.get_variables(event_dict)
        for variable in variables:
            if variable in msg:
                msg = msg.replace(variable, str(variables[variable]))
        return msg

    def get_variables(self, event_dict):
        variables = {}
        for item in event_dict:
            if isinstance(event_dict[item], dict):
		elements = self.get_variables(event_dict[item])
                for element in elements:
                    variables[item.upper()+"."+element.upper()] = elements[element]
            else:
                variables[item.upper()] = event_dict[item]
        return variables

    def get_site_settings_form(self):
        return self.datastore.load_form(forms.SiteSettingsForm, KEY_SITE_SETTINGS)

    def get_site_settings(self):
        return self.get_site_settings_form().initial

    def save_site_settings_form(self, form):
        self.datastore.save_form(form, KEY_SITE_SETTINGS)

    def slack_config(self):
        settings   = self.get_site_settings()
        token      = settings.get('slack_token', '').strip()
        team       = settings.get('slack_team', '').strip()
        channel    = settings.get('slack_channel', '').strip()
        channel_id = settings.get('slack_channel_id', '').strip()
        botname    = settings.get('slack_botname', '').strip()

        return { "token": token, "team": team, "channel": channel, "channel_id": channel_id, "botname": botname }
