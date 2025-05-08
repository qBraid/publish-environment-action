# Copyright (C) 2025 qBraid
#
# This file is part of the qBraid/publish-environment-action
#
# The qBraid/publish-environment-action is free software released under the GNU General Public License v3
# or later. You can redistribute and/or modify it under the terms of the GPL v3.
# See the LICENSE file in the project root or <https://www.gnu.org/licenses/gpl-3.0.html>.
#
# THERE IS NO WARRANTY for the qBraid/publish-environment-action, as per Section 15 of the GPL v3.

"""
Script to create and request to publish a new environment on qBraid.

Requires the following environment variables:
- ENV_CONFIG_PATH: Path to the environment configuration file.
- PERSIST_ENV: Boolean value indicating whether to persist the environment.
- GITHUB_ENV: Path to the GitHub environment file where the environment slug will be written.

"""

import os
import sys

from qbraid_core.services.environments.client import EnvironmentManagerClient
from qbraid_core.services.environments.schema import EnvironmentConfig


def load_environment_config(config_path: str) -> EnvironmentConfig:
    """Loads environment configuration from YAML file."""
    if not os.path.exists(config_path):
        print(f"Environment configuration file not found at {config_path}")
        sys.exit(1)

    print(f"Loading environment configuration from {config_path}...")
    try:
        config = EnvironmentConfig.from_yaml(config_path)
        print("Successfully validated environment configuration data.")
        return config
    except Exception as e:
        print(f"Failed to load environment configuration: \n\t{e}")
        sys.exit(1)


def publish_environment(config: EnvironmentConfig, persist_env: bool) -> str:
    """Publishes the environment and retrieves the environment slug."""
    try:
        client = EnvironmentManagerClient()
        response = client.remote_publish_environment(
            config=config, persist_env=persist_env
        )
        env_slug = response["envSlug"]
        print("Request validated. Initializing environment creation process...")
        print(f"Environment slug: {env_slug}")
        return env_slug
    except Exception as e:
        print(f"Error in environment publish request: \n\t{e}")
        sys.exit(1)


def write_slug_to_github_env(gh_env_path: str, env_slug: str) -> None:
    """Writes the environment slug to the GitHub environment file."""
    if gh_env_path:
        with open(gh_env_path, "a", encoding="utf-8") as f:
            f.write(f"ENV_SLUG={env_slug}\n")


def main():
    config_path = os.getenv("ENV_CONFIG_PATH", "")
    persist_env = os.getenv("PERSIST_ENV", "false")
    gh_env_path = os.getenv("GITHUB_ENV", "")

    if not config_path:
        print("ENV_CONFIG_PATH environment variable not set.")
        sys.exit(1)

    persist_env_bool = persist_env.lower() == "true"

    config = load_environment_config(config_path)
    env_slug = publish_environment(config, persist_env_bool)
    write_slug_to_github_env(gh_env_path, env_slug)


if __name__ == "__main__":
    main()
