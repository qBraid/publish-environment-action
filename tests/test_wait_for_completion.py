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
This module contains unit tests for the functions in the wait_for_completion.py script.
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Add src directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.wait_for_completion import main, wait_for_environment_publish


class TestWaitForCompletion:

    def test_wait_for_environment_publish_success(self):
        # Arrange
        mock_client = MagicMock()
        mock_client.wait_for_env_remote_publish.return_value = True
        env_slug = "test-env-slug"

        # Act
        result = wait_for_environment_publish(mock_client, env_slug)

        # Assert
        mock_client.wait_for_env_remote_publish.assert_called_once_with(env_slug)
        assert result is True

    def test_wait_for_environment_publish_failure(self):
        # Arrange
        mock_client = MagicMock()
        mock_client.wait_for_env_remote_publish.return_value = False
        env_slug = "test-env-slug"

        # Act
        result = wait_for_environment_publish(mock_client, env_slug)

        # Assert
        mock_client.wait_for_env_remote_publish.assert_called_once_with(env_slug)
        assert result is False

    def test_wait_for_environment_publish_error(self, capfd):
        # Arrange
        mock_client = MagicMock()
        mock_client.wait_for_env_remote_publish.side_effect = Exception("API error")
        env_slug = "test-env-slug"

        # Act/Assert
        with pytest.raises(SystemExit):
            wait_for_environment_publish(mock_client, env_slug)

        # Check error message
        out, _ = capfd.readouterr()
        assert "Error in environment publish request" in out
        assert "API error" in out

    @patch("src.wait_for_completion.EnvironmentManagerClient")
    @patch("src.wait_for_completion.wait_for_environment_publish")
    def test_main_success(self, mock_wait, mock_client_cls, setup_env_vars):
        # Arrange
        mock_client = mock_client_cls.return_value
        mock_wait.return_value = True

        # Act
        with patch("sys.exit") as mock_exit:
            main()

        # Assert
        mock_wait.assert_called_once_with(mock_client, "test-env-slug")
        mock_exit.assert_called_once_with(0)

    @patch("src.wait_for_completion.EnvironmentManagerClient")
    @patch("src.wait_for_completion.wait_for_environment_publish")
    def test_main_failure(self, mock_wait, mock_client_cls, setup_env_vars):
        # Arrange
        mock_client = mock_client_cls.return_value
        mock_wait.return_value = False

        # Act
        with patch("sys.exit") as mock_exit:
            main()

        # Assert
        mock_wait.assert_called_once_with(mock_client, "test-env-slug")
        mock_exit.assert_called_once_with(1)

    @patch("os.getenv", return_value="")
    def test_main_missing_env_slug(self, mock_getenv, capfd):
        # Act/Assert
        with pytest.raises(SystemExit):
            main()

        # Check error message
        out, _ = capfd.readouterr()
        assert "ENV_SLUG environment variable not set" in out
