# MIT License
#
# Copyright (c) 2025 qBraid
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Script to poll the status and await the completion of an environment publish request on qBraid.

Requires the following environment variable:
- ENV_SLUG: The slug of the environment for which to poll the publish status.

"""

import os
import sys

from qbraid_core.services.environments.client import EnvironmentManagerClient


def wait_for_environment_publish(client: EnvironmentManagerClient, env_slug: str) -> bool:
    """Waits for the environment to be published and returns the exit code."""
    try:
        print(f"Waiting for publishing process to complete for environment: {env_slug}...")
        success = client.wait_for_env_remote_publish(env_slug)
        print(f"Publish environment process {'completed successfully' if success else 'failed'}")
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
