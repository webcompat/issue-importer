#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import json
import jsonschema
import os
import re
import requests

from config import REPO_URI, OAUTH_TOKEN
from schema import SCHEMA
from termcolor import cprint


def create_issue(payload):
    headers = {'Authorization': 'token {0}'.format(OAUTH_TOKEN)}
    uri = 'https://api.github.com/repos/{0}/issues'.format(REPO_URI)
    r = requests.post(uri, data=json.dumps(payload, ensure_ascii=True),
                           headers=headers)
    cprint(r.json()['html_url'] + ' successfully imported', 'green')


def get_as_json(file_name):
    return json.load(open(file_name))


def validate_json(file_name):
    json_data = get_as_json(file_name)
    try:
        jsonschema.validate(json_data, SCHEMA)
    except jsonschema.exceptions.ValidationError as e:
        print(cprint('JSON Schema validation failed:', 'white', 'on_red'))
        print(e)
    print(json_data)


def get_labels():
    '''Returns all labels in use for the given repo at REPO_URI.'''
    uri = 'https://api.github.com/repos/{0}/labels'.format(REPO_URI)
    labels = []
    r = requests.get(uri)
    for label in r.json():
        labels.append(label.get('name'))
    print('All labels: {0}'.format(labels))
    return labels


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('issue_file',
                        help='JSON file representing a single issue.')
    args = parser.parse_args()
    issue_file = args.issue_file
    validate_json(issue_file)
