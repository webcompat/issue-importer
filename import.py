#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''Main entry point to the importer module.'''

import argparse
import sys
from importer import validate_json, print_labels

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('issue_file', nargs='?', default=sys.stdin,
                        help='JSON file representing a single issue.')
    parser.add_argument('-l', '--labels', action='store_true',
                        help='Print all labels used by issues.')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Don\'t validate labels against the issues repo.')
    args = parser.parse_args()
    if args.labels:
        print_labels()
        sys.exit(0)
    validate_json(args.issue_file, args.force)
