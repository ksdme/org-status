from IGitt.GitHub.GitHub import GitHubToken
from IGitt.GitHub.GitHubOrganization import GitHubOrganization

from org_status.org_hosts import OrgHost, RepoStatus
from org_status.status_providers.travis import TravisBuildStatus


class GitHubOrg(OrgHost):
    HostName = 'github'
    StatusProvider = TravisBuildStatus

    def __init__(self, token, group, **kargs):
        super().__init__(**kargs)

        self._group = group
        self._token = GitHubToken(token)
        self._org = GitHubOrganization(self._token, self._group)

        self._status_provider = self.StatusProvider(self._group)

    def process_repository(self, repo, branch='master'):
        self.print_status(repo.web_url)

        # reliable enough?
        repo_name = repo.web_url.split('/')[-1]
        repo_status = self._status_provider.get_status(repo_name, branch=branch)

        return RepoStatus(repo.web_url, repo_status)

    @property
    def repositories(self):
        return self._org.repositories
