import requests

from org_status.status_providers import StatusProvider, Status


class TravisBuildStatus(StatusProvider):
    BadgeTemplate = ('https://api.travis-ci.org/{group}'
                     '/{repo}.svg?branch={branch}')

    def get_status(self, repo, branch='master'):
        badge_result = requests.get(self.get_badge_url(repo, branch=branch))

        if badge_result.status_code != 200:
            return Status.UNDETERMINED

        return self.status_from_badge_svg(badge_result.text)
