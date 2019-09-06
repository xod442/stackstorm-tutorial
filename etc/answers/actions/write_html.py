#!/usr/bin/env python
#
# Description:
#   Gets a link for a picture. And writes a html link to an index file..
# Author:
#   Rick Kauffman wookieware.com
import os
import argparse
import json
import requests


class WriteHtml(Action):

    def run(self,link):
        params = {'api_key': api_key,
                  'hd': hd}
        if link is not None:
            # write to a index file
            file1=open("/etc/index.html","w")
            line = "<a href="+link+">"+link+"</a>"

            file1.write(line)
            file1.close()

        else:
            error = 'Failed to write link to index file'
            return error
        return link
