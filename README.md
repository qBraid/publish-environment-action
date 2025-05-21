# <img src="icon.png" height=60px align='center'> qBraid Publish Environment Action

GitHub Action to create and request to publish a new environment on qBraid.

## Overview

This action automates the process of publishing Python environments to the qBraid platform. It takes a YAML configuration file and publishes the environment remotely to qBraid. The action requires a [qBraid API key](https://docs.qbraid.com/home/account#api-keys) to authenticate with the qBraid platform. The action can either be auto-triggered on release, manually triggered by the users, triggered via a push to the main branch, or other GitHub events.

## Usage

```yaml
uses: qBraid/publish-environment-action@v1
with:
  api-key: ${{ secrets.QBRAID_API_KEY }}
  environment-file: '.qbraid.yaml'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `api-key` | qBraid API key | Yes | - |
| `environment-file` | Path to the YAML config file | No | `.qbraid.yaml` |
| `wait-for-completion` | Wait for the environment to be published | No | `false` |
| `persist-env` | Persist the environment in qBraid account after the workflow ends | No | `false` |

## Example

- Create a new workflow file `.github/workflows/qbraid-env.yml` 
- Add a secret to the repository with the name `QBRAID_API_KEY` and the value set to your [qBraid API key](https://docs.qbraid.com/home/account#api-keys). See [how to add a secret to a GitHub repository](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository).
- Add the following content to the workflow file to trigger the action manually:

```yaml
name: Publish Environment on qBraid
on:
  workflow_dispatch:

jobs:
  publish_env:
    runs-on: ubuntu-latest 
    steps:
      - name: Publish Environment
        uses: qBraid/publish-environment-action@v1.0.0
        with:
          api-key: ${{ secrets.QBRAID_API_KEY }}
          environment-file: .qbraid.yaml
          wait-for-completion: false
          persist-env: false
```

- The above workflow will:
  * Read the environment configuration from the `.qbraid.yaml` file. 
  * Immediately return after submitting the request to publish the environment.
  * Remove the environment from the qBraid account after the workflow ends.

- Add a file `.qbraid.yaml` to the root of your repository with the details of the environment. For example:

```yaml
# Sample qBraid environment configuration
name: "example-environment"
description: "Environment for testing environment publish action."
tags:
  - "qbraid"
  - "environment"

# add path to the icon file in the repository (optional)
icon: "icon.png"

python_version: "3.11.6"
kernel_name: "Python 3 [name-of-kernel]"
shell_prompt: "shell_prompt"

python_packages:
  # add your package name and optional version
  your_package: ""

  # add any other python packages that may be useful
  numpy: "1.21.2"
  pandas: ">=1.3.3"

```
- Add the icon file `icon.png`, which will be used as the environment icon in qBraid, to your repository and add the path to the icon file in the `.qbraid.yaml` file.
- Commit the changes to the repository.
- Navigate to the Actions tab in your repository and click on the `Publish Environment on qBraid` workflow. Click on the `Run workflow` button for running the action.
