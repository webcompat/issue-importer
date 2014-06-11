## Webcompat Issue Importer

This tool allows importing of issues from external sources to the webcompat.com web-bugs repo.

If you're interested in doing this, please reach out to miket@mozilla.com so he can give your GitHub username push rights to the repo (otherwise this tool won't work).

### JSON schema

See `schema.py` for a description of the expected format of an issue to be imported.

### Usage
1) Install dependencies

`pip install -r requirements.txt`

2) Create a `config.py` file, and add a valid [OAuth token](https://help.github.com/articles/creating-an-access-token-for-command-line-use).

`cp config.py.example config.py`

3) Point the tool to a valid JSON file which contains a single issue. The importer will let you know if the JSON isn't valid.

`python import.py issue.json`

If successful, the tool will print the URL of the newly created issue.
If there's a JSON schema error, a description of the error will be printed.
If there's some kind of other error, the response status code the GitHub API returned will be printed. The [GitHub API documentation](https://developer.github.com/v3/) is helpful in these cases.

To print all the labels used in the repo's issues:

`python import.py -l`

### Running Tests

Use the `nosetests` command.

### License

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.