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

### Organizations

#### List Organizations

```shell
$ circleci-audit orgs
org-1 github
org-2 bitbucket
```

### Repositories

#### List Repositories

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

#### List Repositories' Environment Variables

For all organizations and repositories:

```shell
$ circleci-audit repos vars
org-1 repo-1 env-1
org-2 repo-2 env-2
```

For all repositories in a specific organization:

```shell
$ circleci-audit repos vars --org=org-1
repo-1 env-1
repo-2 env-2
```

For a specific repository:

```shell
$ circleci-audit repos vars --org=org-1 --repo=repo-1
env-1
env-2
```

#### List Repositories' SSH Keys

For all organizations and repositories:

```shell
$ circleci-audit repos keys
org-1 repo-1 github-deploy-key key:finger:print
org-2 repo-2 ssh-key key:finger:print
```

For all repositories in a specific organization:

```shell
$ circleci-audit repos keys --org=org-1
repo-1 github-deploy-key key:finger:print
repo-2 ssh-key key:finger:print
```

For a specific repository:

```shell
$ circleci-audit repos keys --org=org-1 --repo=repo-1
github-deploy-key key:finger:print
ssh-key key:finger:print
```

#### List Repositories' Configured With Jira

List all repositories that have been configured with a secret token to authenticate to Jira.

For all organizations and repositories:

```shell
$ circleci-audit repos jira
org-1 repo-1
org-2 repo-2
```

For all repositories in a specific organization:

```shell
$ circleci-audit repos keys --org=org-1
repo-1
repo-2
```

### Contexts

#### List

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

#### List Contexts' Environment Variables

For all organizations and contexts:

```shell
$ circleci-audit contexts vars
org-1 context-1 env-1
org-2 context-2 env-2
```

For all contexts in a specific organization:

```shell
$ circleci-audit repos vars --org=org-1
context-1 env-1
context-2 env-2
```

For a specific context:

```shell
$ circleci-audit repos vars --org=org-1 --context=context-1
env-1
env-2
```