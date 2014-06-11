#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''Main entry point to the importer module.'''

import argparse
import sys
from importer import validate_json, get_labels

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('issue_file', nargs='?', default=sys.stdin,
                        help='JSON file representing a single issue.')
    parser.add_argument('-l', '--labels', action='store_true',
                        help='Print all labels used by issues.')
    args = parser.parse_args()
    issue_file = args.issue_file
    if args.labels:
        get_labels()
        sys.exit(0)
    validate_json(issue_file)
