#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''Defines a schema to validate against:

body: required, a string
title: required, a string
labels: optional, but if included, all strings
'''

SCHEMA = {
    "type": "object",
    "properties": {
        "body": {"type": "string"},
        "title": {"type": "string"},
        "labels": {
            "type": "array",
            "items": {
                "type": "string"
            }

        },
    },
    "required": ["body", "title"]
}
