#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient class
"""
import unittest
from unittest.mock import patch, MagicMock, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from requests.exceptions import HTTPError
from client import GithubOrgClient, get_json
from typing import Dict, List


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch("client.get_json")
    def test_org(
            self, org: str, resp: Dict,
            mocked_get_json: MagicMock) -> None:
        """Test that GithubOrgClient.org returns the correct value."""
        mocked_get_json.return_value = resp
        client = GithubOrgClient(org)
        self.assertEqual(client.org, resp)
        mocked_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org}"
        )

    def test_public_repos_url(self) -> None:
        """Test the _public_repos_url property."""
        with patch(
            "client.GithubOrgClient.org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/users/google/repos"
            }
            client = GithubOrgClient("google")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/users/google/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Test the public_repos method."""
        repos_payload = [
            {"name": "episodes.dart"},
            {"name": "kratu"},
        ]
        mock_get_json.return_value = repos_payload
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = (
                "https://api.github.com/users/google/repos"
            )
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), ["episodes.dart", "kratu"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': "bsd-3-clause"}}, "bsd-3-clause", True),
        ({'license': {'key': "bsl-1.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(
        self, repo: Dict, license_key: str, expected: bool
    ) -> None:
        """Test the has_license method."""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {
        'org_payload': {
            'login': 'google',
            'repos_url': 'https://api.github.com/orgs/google/repos'
        },
        'repos_payload': [
            {'name': 'repo1', 'license': {'key': 'apache-2.0'}},
            {'name': 'repo2', 'license': {'key': 'apache-2.0'}},
            {'name': 'repo3', 'license': {'key': 'mit'}},
        ],
        'expected_repos': ['repo1', 'repo2', 'repo3'],
        'apache2_repos': ['repo1', 'repo2'],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for the GithubOrgClient class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class fixtures before running tests."""
        cls.route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }
        cls.get_patcher = patch(
            "requests.get", side_effect=cls.mocked_requests_get
        )
        cls.get_patcher.start()

    @classmethod
    def mocked_requests_get(cls, url: str):
        """Mock the requests.get method to return the appropriate payload."""
        if url in cls.route_payload:
            return Mock(**{'json.return_value': cls.route_payload[url]})
        return HTTPError

    @classmethod
    def tearDownClass(cls) -> None:
        """Remove class fixtures after running all tests."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test the public_repos method."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test the public_repos method with a license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"), self.apache2_repos
        )
