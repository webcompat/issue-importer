#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''Does the main work to prepare and create a new issue.'''

import argparse
import json
import jsonschema
import os
import re
import requests

from config import REPO_URI, OAUTH_TOKEN
from schema import schema
from termcolor import cprint


def get_body(json_data):
    '''Return the issue body in the proper format.'''
    body = u'''
**URL**: {0}
**Browser**: {1}
**Version**: {2}

{3}'''
    return body.format(json_data['url'],
                       json_data['browser'],
                       json_data['version'],
                       json_data['body'])


def get_payload(json_data):
    '''Create the POST "payload" object.'''
    payload = {}
    payload['body'] = get_body(json_data)
    payload['title'] = json_data['title']
    payload['labels'] = json_data['labels']
    return payload


def create_issue(json_data):
    '''Create a new GitHub issue by POSTing data to the issues API endpoint.
    If successful, the URL to the new issue is printed. Otherwise, the error
    code is printed.'''
    headers = {
        'Authorization': 'token {0}'.format(OAUTH_TOKEN),
        'User-Agent': 'Webcompat-Issue-Importer'
    }
    payload = get_payload(json_data)
    uri = 'https://api.github.com/repos/{0}/issues'.format(REPO_URI)
    r = requests.post(uri, data=json.dumps(payload), headers=headers)
    if r.status_code != 201:
        cprint('Something went wrong. Response: {0}. See '
               'developer.github.com/v3/ for troubleshooting.'.format(
                   r.status_code), 'red')
        return False
    else:
        cprint(r.json()['html_url'] + ' successfully imported', 'green')
        return True


def get_as_json(issue_file):
    '''Return the contents of `issue_file` as a JSON object.'''
    try:
        # is `issue_file` a file object?
        r = json.load(issue_file)
    except AttributeError:
        # is `issue_file` a file name (string)?
        r = json.load(open(issue_file))
    return r


def validate_json(issue_file):
    '''Validate the structure of `file_name` against our JSON schema.'''
    json_data = get_as_json(issue_file)
    try:
        jsonschema.validate(json_data, schema)
        create_issue(json_data)
    except jsonschema.exceptions.ValidationError as e:
        cprint('JSON Schema validation failed:', 'white', 'on_red')
        print(e)


def get_labels():
    '''Returns all labels in use for the given repo at REPO_URI.'''
    uri = 'https://api.github.com/repos/{0}/labels'.format(REPO_URI)
    labels = []
    r = requests.get(uri)
    for label in r.json():
        labels.append(label.get('name'))
    return labels


def print_labels():
    '''Print all labels used by issues at REPO_URI.'''
    print('All labels: {0}'.format(get_labels()))
