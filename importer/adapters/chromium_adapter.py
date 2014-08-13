#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import json
import re
import requests
import sys
from xmltodict import parse

# This is a deprecated API. So who knows how long it will exist for.
ISSUES_URI = 'https://code.google.com/feeds/issues/p/chromium/issues/'
ENTRY_URI = ISSUES_URI + 'full/{0}'
COMMENTS_URI = ISSUES_URI + '{0}/comments/full'


def get_xml(uri):
    '''Make a GET request to the issue API endpoint. Get a boatload
    of XML back.'''
    r = requests.get(uri)
    return r.text


def get_body(response):
    '''Get the issue body text (which is html). Also add a link back
    to the original crbug issue.'''
    body = response.get('entry').get('content').get('#text')
    href = response.get('entry').get('link')[1].get('@href')
    if 'http://code.google.com/p/chromium/issues/detail?id' in href:
        body += '\n\n[Original Chromium bug tracker issue]({0}).'.format(href)
    return body


def get_url(response):
    '''Attempt to parse the URL out of the bug body, but only looking for
    "URLs (if applicable) :". No attempt at URL validation is done.'''
    body = get_body(response)
    match = re.search(r'URLs\s(?:\(if\sapplicable\))?\s?:(.+)$', body,
                      flags=re.I | re.M)
    if match:
        return match.group(1)
    else:
        return 'Unknown (possibly in description)'
    pass


def get_os(response):
    '''Attempt to parse the operating system out of the bug body, but only
    looking for "OS:".'''
    body = get_body(response)
    match = re.search(r'OS\s?:(.+)$', body, flags=re.I | re.M)
    if match:
        return match.group(1)
    else:
        return 'Unknown (possibly in description)'
    pass


def get_browser(response):
    '''Attempt to parse the browser version out of the bug body.
    Seems like this is expressed in a lot of different ways looking at
    different bugs, so fall back to "unknown" if we can't match on
    "Version :\n".'''
    body = get_body(response)
    match = re.search(r'(?:Chrome\s)?Version\s+:\s+(.+)$', body,
                      flags=re.I | re.M)
    if match:
        return match.group(1)
    else:
        return 'Unknown (possibly in description)'


def get_comments(issue_id):
    comments_xml = get_xml(COMMENTS_URI.format(issue_id))
    response = parse(comments_xml)

    def get_id(c):
        '''Pull the comment id number out of its id URI'''
        id_uri = c.get('id')
        id = id_uri.rsplit('/', 1)[1]
        return int(id)

    def get_comment(c):
        '''Get the comment text and add a link back + author.'''
        href = c.get('link')[0].get('@href')
        body = c.get('content').get('#text')
        author = c.get('author').get('name')
        author_link = 'https://code.google.com' + c.get('author').get('uri')
        return '[Original comment #{0}]({1}) by [{2}]({3})\n___\n\n{4}'.format(
            get_id(c), href, author, author_link, body)

    ordered = sorted(response.get('feed').get('entry'), key=get_id)
    f = [get_comment(c) for c
         in ordered
         if c.get('content').get('#text') is not None]

    return f


def adapt(issue_id):
    '''Convert the Chromium issue XML into a JSON data structure that works
    with the webcompat issue importer.'''
    xml = get_xml(ENTRY_URI.format(issue_id))
    response = parse(xml)
    try:
        issue = {
            'body': get_body(response),
            'browser': get_browser(response),
            'comments': get_comments(issue_id),
            'labels': ['chrome', 'imported'],
            'os': get_os(response),
            'title': response.get('entry').get('title'),
            'url': get_url(response),
        }
        print(json.dumps(issue))
    except Exception as e:
        print(e)
        sys.exit('Something went wrong :(.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('issue_id', type=int,
                        help='Chromium tracker issue id (number).')
    args = parser.parse_args()
    adapt(args.issue_id)
