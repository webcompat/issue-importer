#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''Test failure in issue creation.'''

import requests
import unittest

from importer import create_issue
from httmock import urlmatch, HTTMock

payload = {
  u"url": u"www.💩.com",
  u"title": u"Upgrade browser message",
  u"browser": u"Firefox",
  u"version": u"30",
  u"body": u"The site asks me to upgrade",
  u"labels": [u"contactready", u"invalid"]
}


@urlmatch(netloc=r'api\.github\.com$')
def github_post_mock(url, request):
    return {'status_code': 401,
            'content': "Go away."}

class TestPostSuccess(unittest.TestCase):
    def test_issues_redirect(self):
        with HTTMock(github_post_mock):
            self.assertFalse(create_issue(payload))


if __name__ == '__main__':
    unittest.main()
