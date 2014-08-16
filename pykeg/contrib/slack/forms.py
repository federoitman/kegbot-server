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

"""Webhook plugin forms."""

from django import forms

TEXTAREA = forms.Textarea(attrs={'class': 'input-block-level'})
TEXTFIELD = forms.Textarea(attrs={'class': 'input-block-level', 'cols': 80, 'rows': 1})


class SiteSettingsForm(forms.Form):
    slack_token      = forms.CharField(required=True, widget=TEXTFIELD)
    slack_team       = forms.CharField(required=True, widget=TEXTFIELD)
    slack_channeli   = forms.CharField(required=True, widget=TEXTFIELD)
    slack_channel_id = forms.CharField(required=True, widget=TEXTFIELD)
    slack_botname    = forms.CharField(required=True, widget=TEXTFIELD)
    drink_poured_msg = forms.CharField(required=False, widget=TEXTAREA,
        help_text='Message to send for new pour')
