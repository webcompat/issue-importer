#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''Defines a schema to validate against:

url: required, a string
title: required, a string
browser: required, a string
version: required, a string
body: required, a string
labels: optional, but if included, all strings
'''

schema = {
    "type": "object",
    "properties": {
        "url": {"type": "string"},
        "title": {"type": "string"},
        "browser": {"type": "string"},
        "version": {"type": "string"},
        "body": {"type": "string"},
        "labels": {
            "type": "array",
            "items": {
                "type": "string"
                # enum of allowed values added dynamically
                # unless the --force option is used.
            }
        },
        "comments": {
            # comments, if included, should be ordered from old to new
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["url", "title", "browser", "version", "body"]
}
