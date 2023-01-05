# CircleCI Audit

## Pre-requisites:

* Python 3.7+

## Setup

### Create a CircleCI Personal Token

Follow [these instructions](https://circleci.com/docs/managing-api-tokens/#creating-a-personal-api-token).

This token is used by `circleci-audit` to authenticate with the CircleCI API. `circleci-audit` can only access
repositories that are accessible to the account that owns this personal API token.

### Install `circleci-audit`:

```shell
$ python3 -m pip install circleci-audit
$ export CIRCLECI_AUDIT_TOKEN="your personal token"
$ export CIRCLECI_AUDIT_ORGANIZATION="your organization name"
$ circleci-audit validate
All required configuration provided
CIRCLECI_AUDIT_TOKEN = REDACTED
CIRCLECI_AUDIT_ORGANIZATION = your organization name
CIRCLECI_AUDIT_VCS_NAME = github
CIRCLECI_AUDIT_VCS_SLUG = gh
```

## Commands

### List Repositories

```shell
$ circleci-audit repos
example https://github.com/your-org/example
another-example https://github.com/your-org/another-example
```