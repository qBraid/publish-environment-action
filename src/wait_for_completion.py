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
Script to poll the status and await the completion of an environment publish request on qBraid.

Requires the following environment variable:
- ENV_SLUG: The slug of the environment for which to poll the publish status.

"""

import os
import sys

from qbraid_core.services.environments.client import EnvironmentManagerClient


def wait_for_environment_publish(
    client: EnvironmentManagerClient, env_slug: str
) -> bool:
    """Waits for the environment to be published and returns the exit code."""
    try:
        print(
            f"Waiting for publishing process to complete for environment: {env_slug}..."
        )
        success = client.wait_for_env_remote_publish(env_slug)
        print(
            f"Publish environment process {'completed successfully' if success else 'failed'}"
        )
        return success
    except Exception as e:
        print(f"Error in environment publish request: \n\t{e}")
        sys.exit(1)


def main():
    env_slug = os.getenv("ENV_SLUG", "")

    if not env_slug:
        print("ENV_SLUG environment variable not set.")
        sys.exit(1)

    client = EnvironmentManagerClient()

    success = wait_for_environment_publish(client, env_slug)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
