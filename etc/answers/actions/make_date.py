#!/usr/bin/env python
#
# Description:
#   a stackstorm action that takes a link string and formats as a hypelink and
#   writes to the /etc/index.html.
# Author:
#   Rick Kauffman wookieware.com
import datetime

from st2common.runners.base_action import Action


class Make_Date(Action):

    def run(self):
        now=datetime.datetime.now()
        date=(now.strftime("%Y-%m-%d"))
        return date
