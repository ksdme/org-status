## How it works?
`travis-org-status` uses repo SVG labels to determine status of the repo build.

## Usage

```
GITHUB_TOKEN=[GH_TOKEN] python org-status.py [ORG-NAME]
```

Organization has to be in scope of the access token. If it is a public org then `repo` scope should be sufficient. Use `--no-color` for no colored mode.

## Result
```shell
https://github.com/coala/coala-vs-code: passing
https://github.com/coala/coala-quickstart: failing
https://github.com/coala/rultor-python: failing
https://github.com/coala/devops: passing
https://github.com/coala/bear-docs: failing
https://github.com/coala/docker-coala-base: None
https://github.com/coala/projects: failing
https://github.com/coala/coala-html: passing
https://github.com/coala/coala-ls: failing
https://github.com/coala/community: passing
https://github.com/coala/coala-bears: failing
https://github.com/coala/gh-board: failing
https://github.com/coala/git-task-list: passing
https://github.com/coala/coala-eclipse: failing
https://github.com/coala/PyPrint: passing
https://github.com/coala/coala: failing
https://github.com/coala/coala-emacs: failing
https://github.com/coala/documentation: failing
https://github.com/coala/corobo: passing
https://github.com/coala/gci-leaders: failing
https://github.com/coala/landing-frontend: passing
8 Passing, 12 Failing, 33 Unknown of 54 Repositories
```
