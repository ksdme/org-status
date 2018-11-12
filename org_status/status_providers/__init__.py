from enum import Enum


class Status(Enum):
    ERROR = 'error'
    UNKNOWN = 'unknown'
    FAILING = 'failing'
    PASSING = 'passing'
    UNDETERMINED = 'undetermined'


StatusVariants = {
  Status.ERROR:   ('error',),
  Status.FAILING: ('failing', 'failed'),
  Status.PASSING: ('passing', 'passed'),
  Status.UNKNOWN: ('unknown',),
}


class StatusProvider:
    NAME = None
    BadgeTemplate = None

    def __init__(self, group):
        if self.BadgeTemplate is None:
            raise NotImplementedError()

        self._group = group
        self._group_url = self.BadgeTemplate.format(
          group=group, repo='{repo}', branch='{branch}', host='{host}')

    def get_badge_url(self, repo, host, branch='master'):
        return self._group_url.format(repo=repo, branch=branch, host=host)

    def status_from_badge_svg(self, svg):
        svg = svg.lower()

        for status, variants in StatusVariants.items():
            for variant in variants:
                if variant in svg:
                    return status

    @classmethod
    def get_status_provider_status(self):
        raise NotImplementedError()


def get_supported_status_providers():
    from org_status.status_providers.travis import TravisBuildStatus
    from org_status.status_providers.gitlab_ci import GitLabCIStatus
    from org_status.status_providers.appveyor import AppVeyorStatus

    return (
        TravisBuildStatus,
        GitLabCIStatus,
        AppVeyorStatus,
    )
