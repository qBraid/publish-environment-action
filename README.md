# <img src="./icon.png" alt="qBraid" height="45" style="vertical-align: middle;"/> publish-environment-action

GitHub Action to remotely publish qBraid environments

## Overview

This action automates the process of publishing Python environments to the qBraid platform. It takes a YAML configuration file and publishes the environment remotely to qBraid. The action requires a qBraid API key to authenticate with the qBraid platform. The action can either be auto-triggered on release, manually triggered by the users, triggered via a push to the main branch, etc. 

## Usage

```yaml
uses: qBraid/publish-environment-action@v1
with:
    env_config_path: <<path to the YAML file>>
    wait_for_completion: <<boolean value>>
    qbraid_api_key: ${{ secrets.QBRAID_API_KEY }}
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `env_config_path` | Path to the YAML file | No | `.qbraid-env.yaml` |
| `qbraid_api_key` | qBraid API key | Yes | - |
| `wait_for_completion` | Wait for the environment publish request to complete | No | `false` |

## Example

### Manually trigger the action
- Create a new workflow file `action.yml` in the `.github/workflows` directory of your project
- Add a secret to the repository with the name `QBRAID_API_KEY` and the value as [the qBraid API key](https://docs.qbraid.com/home/account#api-keys). See [how to add a secret to a GitHub repository](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository)
- Add the following content to the workflow file to trigger the action manually -
```yaml
name: Publish Environment on qBraid
on:
  workflow_dispatch:
    inputs:
      env_config_path:
        description: "Path to the yaml config file"
        required: true
        type: string 
        default: '.qbraid-env.yaml'
      wait_for_completion:
        description: "Wait for the environment to be published"
        required: true
        type: boolean
        default: false

jobs:
  publish_env:
    runs-on: ubuntu-latest 
    steps:
      - name: Publish Environment
        uses: qBraid/publish-environment-action@v1
        with:
          env_config_path: ${{ github.event.inputs.env_config_path }}
          wait_for_completion: ${{ github.event.inputs.wait_for_completion }}
          qbraid_api_key: ${{ secrets.QBRAID_API_KEY }}
```
- Add a file `.qbraid-env.yaml` to the root of your repository with the details of the environment. See example below -
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
kernel_name: "Python 3[name-of-kernel]"
shell_prompt: "shell_prompt"

python_packages:
  # add your package name and version 
  # to publish
  your_package: "package-version-string"

  # add any extra python packages
  numpy: "1.21.2"
  pandas: ">=1.3.3"

```
- Add the icon file `icon.png`, which will be used as the environment icon in qBraid, to your repository and add the path to the icon file in the `.qbraid-env.yaml` file
- Commit the changes to the repository

- Navigate to the Actions tab in your repository and click on the `Publish Environment on qBraid` workflow. Click on the `Run workflow` button and provide the path to the YAML file and the boolean value for `wait_for_completion` for running the action