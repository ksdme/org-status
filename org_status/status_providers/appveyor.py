import requests

from org_status.status_providers import StatusProvider, Status


class AppVeyorStatus(StatusProvider):
    NAME = 'appveyor'
    BadgeTemplate = ('https://ci.appveyor.com/api/projects/status/{host}/'
                     '{group}/{repo}?branch={branch}&svg=true')

    def get_status(self, repo, host, branch='master'):
        badge_result = requests.get(self.get_badge_url(repo,
                                                       host,
                                                       branch=branch))

        if badge_result.status_code != 200:
            return Status.UNDETERMINED

        return self.status_from_badge_svg(badge_result.text)
