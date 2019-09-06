#!/usr/bin/env python
#
# Description:
#   a stackstorm action that takes a link string and formats as a hypelink and
#   writes to the /etc/index.html.
# Author:
#   Rick Kauffman wookieware.com
import os
import argparse
import json
import requests
from st2common.runners.base_action import Action


class WriteHtml(Action):

    def run(self,link):
        if link is not None:
            # write to a index file
            file1=open("/opt/stackstorm/packs/tutorial/etc/index.html","a")
            line = "<p><a href="+link+">"+link+"</a></p>\n"

            file1.write(line)
            file1.close()

        else:
            error = 'Failed to write link to index file'
            return error
        return link
