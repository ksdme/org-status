import responses

from org_status.org_hosts.github import GitHubOrg
from org_status.org_hosts.gitlab import GitLabOrg


@responses.activate
def test_github_get_org_status():
    up_json = {'status': 'good'}
    down_json = {'status': 'down'}

    responses.add(responses.GET, 'https://status.github.com/api/status.json',
                  json=up_json)
    responses.add(responses.GET, 'https://status.github.com/api/status.json',
                  json=down_json)

    assert GitHubOrg.get_host_status() is True
    assert GitHubOrg.get_host_status() is False


@responses.activate
def test_gitlab_get_org_status():
    down_json = {'result': {'status_overall': {'status': 'Down'}}}
    up_json = {'result': {'status_overall': {'status': 'Operational'}}}

    responses.add(responses.GET, GitLabOrg.HOST_STATUS_URL,
                  json=up_json)
    responses.add(responses.GET, GitLabOrg.HOST_STATUS_URL,
                  json=down_json)

    assert GitLabOrg.get_host_status() is True
    assert GitLabOrg.get_host_status() is False
