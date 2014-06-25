#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''Test successful issue creation.'''

import requests
import unittest

from importer import create_issue
from httmock import urlmatch, HTTMock

json_data = {
  u"url": u"www.💩.com",
  u"title": u"Upgrade browser message",
  u"browser": u"Firefox 30",
  u"os": u"Windows 7",
  u"body": u"The site asks me to upgrade",
  u"labels": [u"contactready", u"invalid"],
  u"comments": [u"1", u"2", u"3"]
}

mock_post_response = {"url":"https://api.github.com/repos/miketaylr/nobody-look-at-this/issues/62","labels_url":"https://api.github.com/repos/miketaylr/nobody-look-at-this/issues/62/labels{/name}","comments_url":"https://api.github.com/repos/miketaylr/nobody-look-at-this/issues/62/comments","events_url":"https://api.github.com/repos/miketaylr/nobody-look-at-this/issues/62/events","html_url":"https://github.com/miketaylr/nobody-look-at-this/issues/62","id":"35306060","number":"62","title":"Upgrade browser message","user":{"login":"miketaylr","id":"67283","avatar_url":"https://avatars.githubusercontent.com/u/67283?","gravatar_id":"929d3002e426ec2e88d89637d3f5f8ba","url":"https://api.github.com/users/miketaylr","html_url":"https://github.com/miketaylr","followers_url":"https://api.github.com/users/miketaylr/followers","following_url":"https://api.github.com/users/miketaylr/following{/other_user}","gists_url":"https://api.github.com/users/miketaylr/gists{/gist_id}","starred_url":"https://api.github.com/users/miketaylr/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/miketaylr/subscriptions","organizations_url":"https://api.github.com/users/miketaylr/orgs","repos_url":"https://api.github.com/users/miketaylr/repos","events_url":"https://api.github.com/users/miketaylr/events{/privacy}","received_events_url":"https://api.github.com/users/miketaylr/received_events","type":"User","site_admin":"false"},"labels":[{"url":"https://api.github.com/repos/miketaylr/nobody-look-at-this/labels/invalid","name":"invalid","color":"e6e6e6"},{"url":"https://api.github.com/repos/miketaylr/nobody-look-at-this/labels/contactready","name":"contactready","color":"eb6420"}],"state":"open","assignee":"null","milestone":"null","comments":"0","created_at":"2014-06-09T17:40:25Z","updated_at":"2014-06-09T17:40:25Z","closed_at":"null","body":"The site asks me to upgrade","closed_by":"null"}


@urlmatch(netloc=r'api\.github\.com$')
def github_post_mock(url, request):
    return {'status_code': 201,
            'content': mock_post_response}

class TestPostSuccess(unittest.TestCase):
    def test_issues_redirect(self):
        with HTTMock(github_post_mock):
            self.assertTrue(create_issue(json_data))


if __name__ == '__main__':
    unittest.main()
