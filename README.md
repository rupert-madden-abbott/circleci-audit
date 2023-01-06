# CircleCI Audit

## Pre-requisites:

* Python 3.7+

## Setup

### Create a CircleCI Personal Token

Follow [these instructions](https://circleci.com/docs/managing-api-tokens/#creating-a-personal-api-token).

This token is used by `circleci-audit` to authenticate with the CircleCI API. `circleci-audit` can only access
repositories that are accessible to the account that owns this personal API token.

### Install circleci-audit:

```shell
$ python3 -m pip install circleci-audit
$ export CIRCLECI_AUDIT_TOKEN="your personal token"
$ circleci-audit --help
```

## Commands

### List Organizations

```shell
$ circleci-audit orgs
org-1 github
org-2 bitbucket
```

### List Repositories

For all organizations:

```shell
$ circleci-audit repos
org-1 example https://github.com/your-org/example
org-2 another-example https://github.com/your-org/another-example
```

For a specific organization:

```shell
$ circleci-audit repos --org=org-1
example https://github.com/your-org/example
another-example https://github.com/your-org/another-example
```

### List Contexts

For all organizations:

```shell
$ circleci-audit contexts
org-1 example
org-2 another-example
```

For a specific organization:

```shell
$ circleci-audit contexts --org=org-1
example
another-example
```