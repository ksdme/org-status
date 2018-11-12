import json
import requests

from org_status.status_providers import StatusProvider, Status


class TravisBuildStatus(StatusProvider):
    NAME = 'travis'
    BadgeTemplate = ('https://api.travis-ci.org/{group}'
                     '/{repo}.svg?branch={branch}')

    TravisStatusUrl = 'https://pnpcptp8xh9k.statuspage.io/api/v2/status.json'

    def get_status(self, repo, host, branch='master'):
        badge_result = requests.get(self.get_badge_url(repo,
                                                       host,
                                                       branch=branch))

        if badge_result.status_code != 200:
            return Status.UNDETERMINED

        return self.status_from_badge_svg(badge_result.text)

    @classmethod
    def get_status_provider_status(cls):
        try:
            response = requests.get(cls.TravisStatusUrl)
            status = json.loads(response.text)

            description = status['status']['description']
            return description.lower() == 'all systems operational'
        except Exception:
            return None
