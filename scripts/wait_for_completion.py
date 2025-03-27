import os
from qbraid_core.services.environments.client import EnvironmentManagerClient

env_slug = os.getenv("ENV_SLUG")
client = EnvironmentManagerClient()

# Wait for the environment to be published
try:
    success = client.wait_for_env_remote_publish(env_slug)
    print(f"Environment publish completed, status: {success}")
    if not success:
        print("Error in environment publish request")
        response = client.retrieve_remote_publish_status(env_slug)
        print(f"Final publish status: {response}")
        exit(1)
except Exception as e:
    print(f"Error in environment publish request: {e}")
    exit(1)
