#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''Tests related to importing comments.'''

import requests
import unittest

from importer import add_comment

json_data = {
  u"url": u"www.💩.com",
  u"title": u"Upgrade browser message",
  u"browser": u"Firefox 30",
  u"os": u"Windows 7",
  u"body": u"The site asks me to upgrade",
  u"labels": [u"contactready", u"invalid"],
  u"comments": [u"1", u"2", u"", u"3", None]
}

class TestComments(unittest.TestCase):
    def test_empty_comments(self):
        self.assertFalse(add_comment("1", ""))
        self.assertFalse(add_comment("1", None))

if __name__ == '__main__':
    unittest.main()
