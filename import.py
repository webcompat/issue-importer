#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''Main entry point to the importer module.'''

import argparse
from importer import validate_json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('issue_file',
                        help='JSON file representing a single issue.')
    args = parser.parse_args()
    issue_file = args.issue_file
    validate_json(issue_file)
