from IGitt.GitLab.GitLab import GitLabPrivateToken
from IGitt.GitLab.GitLabOrganization import GitLabOrganization

from org_status.org_hosts import OrgHost, RepoStatus
from org_status.status_providers.gitlab_ci import GitLabCIStatus


class GitLabOrg(OrgHost):
    HostName = 'gitlab'
    StatusProvider = GitLabCIStatus

    def __init__(self, token, group, **kargs):
        super().__init__(**kargs)

        self._group = group
        self._token = GitLabPrivateToken(token)
        self._org = GitLabOrganization(self._token, self._group)

        self._status_provider = self.StatusProvider(self._group)

    def process_repository(self, repo, branch='master'):
        self.print_status(repo.web_url)

        # reliable enough?
        repo_name = '/'.join(repo.web_url.split('/')[4:])
        repo_status = self._status_provider.get_status(repo_name,
                                                       self.HostName,
                                                       branch=branch)

        return RepoStatus(repo.web_url, repo_status)

    @property
    def repositories(self):
        return self._org.repositories
