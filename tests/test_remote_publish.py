import os
import sys
from unittest.mock import MagicMock, mock_open, patch

import pytest

# Add src directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.remote_publish import (
    load_environment_config,
    main,
    publish_environment,
    write_slug_to_github_env,
)


class TestRemotePublish:

    @patch("os.path.exists", return_value=True)
    @patch("src.remote_publish.EnvironmentConfig")
    def test_load_environment_config_success(self, mock_env_config, mock_exists):
        # Arrange
        config_path = "path/to/config.yaml"
        mock_config = MagicMock()
        mock_env_config.from_yaml.return_value = mock_config

        # Act
        result = load_environment_config(config_path)

        # Assert
        mock_exists.assert_called_with(config_path)
        mock_env_config.from_yaml.assert_called_with(config_path)
        assert result == mock_config

    @patch("os.path.exists", return_value=False)
    def test_load_environment_config_file_not_found(self, mock_exists, capfd):
        # Arrange
        config_path = "path/to/nonexistent/config.yaml"

        # Act/Assert
        with pytest.raises(SystemExit):
            load_environment_config(config_path)

        # Check error message
        out, _ = capfd.readouterr()
        assert f"Environment configuration file not found at {config_path}" in out

    @patch(
        "src.remote_publish.EnvironmentConfig.from_yaml",
        side_effect=Exception("Test error"),
    )
    @patch("os.path.exists", return_value=True)
    def test_load_environment_config_invalid_yaml(
        self, mock_exists, mock_from_yaml, capfd
    ):
        # Arrange
        config_path = "path/to/invalid/config.yaml"

        # Act/Assert
        with pytest.raises(SystemExit):
            load_environment_config(config_path)

        # Check error message
        out, _ = capfd.readouterr()
        assert "Failed to load environment configuration" in out
        assert "Test error" in out

    @patch("src.remote_publish.EnvironmentManagerClient")
    def test_publish_environment_success(self, mock_client_cls):
        # Arrange
        mock_config = MagicMock()
        mock_client = mock_client_cls.return_value
        mock_client.remote_publish_environment.return_value = {"envSlug": "test-slug"}

        # Act
        result = publish_environment(mock_config, False)

        # Assert
        mock_client.remote_publish_environment.assert_called_with(
            config=mock_config, persist_env=False
        )
        assert result == "test-slug"

    @patch("src.remote_publish.EnvironmentManagerClient")
    def test_publish_environment_error(self, mock_client_cls, capfd):
        # Arrange
        mock_config = MagicMock()
        mock_client = mock_client_cls.return_value
        mock_client.remote_publish_environment.side_effect = Exception("API error")

        # Act/Assert
        with pytest.raises(SystemExit):
            publish_environment(mock_config, True)

        # Check error message
        out, _ = capfd.readouterr()
        assert "Error in environment publish request" in out
        assert "API error" in out

    def test_write_slug_to_github_env(self):
        # Arrange
        gh_env_path = "path/to/github/env"
        env_slug = "test-slug"
        mock_file = mock_open()

        # Act
        with patch("builtins.open", mock_file):
            write_slug_to_github_env(gh_env_path, env_slug)

        # Assert
        mock_file.assert_called_once_with(gh_env_path, "a", encoding="utf-8")
        mock_file().write.assert_called_once_with(f"ENV_SLUG={env_slug}\n")

    @patch("src.remote_publish.load_environment_config")
    @patch("src.remote_publish.publish_environment")
    @patch("src.remote_publish.write_slug_to_github_env")
    def test_main_success(self, mock_write, mock_publish, mock_load, setup_env_vars):
        # Arrange
        mock_config = MagicMock()
        mock_load.return_value = mock_config
        mock_publish.return_value = "test-slug"

        # Act
        main()

        # Assert
        mock_load.assert_called_once_with("path/to/test/config.yaml")
        mock_publish.assert_called_once_with(mock_config, False)
        mock_write.assert_called_once_with("path/to/github/env", "test-slug")

    @patch("os.getenv", return_value="")
    def test_main_missing_config_path(self, mock_getenv, capfd):
        # Act/Assert
        with pytest.raises(SystemExit):
            main()

        # Check error message
        out, _ = capfd.readouterr()
        assert "ENV_CONFIG_PATH environment variable not set" in out
