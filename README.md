# Webcompat Issue Importer

Spec.

Example of Bugzilla Output

Example of Chromium Output

Expected Input:

title: "String",
body: "String, separated by newlines \n". Markdown accepted.,
labels: array of strings

method to validate against existing labels

GET /repos/:owner/:repo/labels
#gets all labels


todo: tests, mocking requests post
validate json?
json schema validation.

3 simple keys... but the output needs to be transformed. Site owner, etc.

take a single argument, a json file,

do schema validation on json file
transform
POST