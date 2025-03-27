import os
from qbraid_core.services.environments.schema import EnvironmentConfig
from qbraid_core.services.environments.client import EnvironmentManagerClient

# Load the environment config
config_path = os.environ["ENV_CONFIG_PATH"]
config = EnvironmentConfig.from_yaml(config_path)
print(f"Successfully validated configuration from {config_path}!")

# Make request to publish
client = EnvironmentManagerClient()
try:
    response = client.remote_publish_environment(
        file_path=config_path, persist_env=os.environ["PERSIST_ENV"]
    )

    # Print the slug and set it as an env variable
    env_slug = response["envSlug"]
    print(f"Successfully published environment with slug: {env_slug}")

    with open(os.getenv("GITHUB_ENV"), "a") as envs_file:
        envs_file.write(f"ENV_SLUG={env_slug}\n")

except Exception as e:
    print(f"Error in environment publish request: {e}")
    exit(1)
