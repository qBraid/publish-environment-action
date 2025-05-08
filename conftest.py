import os
from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_environment_config():
    """Fixture for a mock environment configuration."""
    return Mock(name="Test Environment")


@pytest.fixture
def setup_env_vars():
    """Setup test environment variables and clean them up after test."""
    # Save original environment variables
    original_env = os.environ.copy()

    # Set test environment variables
    os.environ["ENV_CONFIG_PATH"] = "path/to/test/config.yaml"
    os.environ["PERSIST_ENV"] = "false"
    os.environ["GITHUB_ENV"] = "path/to/github/env"
    os.environ["ENV_SLUG"] = "test-env-slug"

    yield

    # Restore original environment variables
    os.environ.clear()
    os.environ.update(original_env)
