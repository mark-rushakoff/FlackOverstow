#!/usr/bin/env python

__author__ = "Mark Rushakoff"
__license__ = "MIT"

import sys
import urllib2
import re
import StringIO
import gzip

try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        sys.stderr.write("simplejson or json required for operation.  Aborting.\n")
        sys.exit()

try:
    from BeautifulSoup import BeautifulStoneSoup as bss
except ImportError:
    sys.stderr.write("BeautifulSoup required to format data")
    sys.stderr.write("Try `easy_install beautifulsoup`")
    sys.exit()

stripHtmlTags = re.compile(r"<[^>]*>")
compressWhiteSpace = re.compile(r"\s+")

def format(text):
    return bss(compressWhiteSpace.sub(' ', stripHtmlTags.sub('', text)), convertEntities=bss.ALL_ENTITIES)

class Grabber(object):
    """ Class to obtain JSON data from Stack API """

    _api = '1.0'

    def __init__(self, site, user_id, api_key=None):
        self.site = site
        self.user_id = user_id
        self.api_key = api_key

    def _grab(self, users_arg):
        url = 'http://api.%s/%s/users/%s/%s?body=true&pagesize=100' % (self.site, self._api, self.user_id, users_arg)
        if self.api_key is not None:
            url += '&key=%s' % self.api_key
        content = StringIO.StringIO(urllib2.urlopen(url).read())
        return gzip.GzipFile(fileobj=content).read()

    def minimal_text(self, users_arg):
        """ return a list of just the simple text of the `body`s of the users_arg section of the pulled json """
        json_data = self._grab(users_arg)
        answers = [answer['body'] for answer in json.loads(json_data)[users_arg]]
        return [str(format(answer)) for answer in answers]

if __name__ == "__main__":
    grabber = Grabber('stackoverflow.com', 126042)
    for g in grabber.minimal_text('answers'):
        print g
