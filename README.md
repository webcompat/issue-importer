## Webcompat Issue Importer

This tool allows importing of issues from external sources to the [web-bugs](http://github.com/webcompat/web-bugs) repo (which allows them to be displayed on webcompat.com).

If you're interested in doing this, please reach out to miket@mozilla.com so he can give your GitHub username push rights to the repo (otherwise this tool won't work).

### JSON schema

The JSON passed in is validated against the following JSON schema:

``` python
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
```

See [http://json-schema.org/](http://json-schema.org/) for more information.

### Setup
1) Install dependencies

`pip install -r requirements.txt`

2) Create a `config.py` file, filling in appropriate values:

`cp importer/config.py.example importer/config.py`

`OAUTH_TOKEN`: A valid [GitHub user commandline token](https://help.github.com/articles/creating-an-access-token-for-command-line-use) that has push access to the repo at `REPO_URI`

`REPO_URI`: `<username>/<repo>`, e.g., `webcompat/web-bugs`.


### Usage

```
usage: import.py [-h] [-l] [-f] [issue_file]

positional arguments:
  issue_file    JSON file representing a single issue.

optional arguments:
  -h, --help    show this help message and exit
  -l, --labels  Print all labels used by issues.
  -f, --force   Don't validate labels against the issues repo.
```

#### Usage Examples

Import an single issue.

`python import.py issue.json`

`cat issue.json | python import.py`

List all labels currently used at `REPO_URI`:

`python import.py -l`


Ignore issue label validation and import issue (unknown labels will be ignored):

`python import.py --force issue.json`

If successful, the tool will print the URL of the newly created issue.
If there's a JSON schema error, a description of the error will be printed.
If there's some kind of other error, the response status code the GitHub API returned will be printed. The [GitHub API documentation](https://developer.github.com/v3/) is helpful in these cases.

### Running Tests

Use the `nosetests` command.

### License

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.