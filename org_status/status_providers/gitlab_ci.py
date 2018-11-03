import requests

from org_status.status_providers import StatusProvider, Status


class GitLabCIStatus(StatusProvider):
    BadgeTemplate = ('https://gitlab.com/{group}'
                     '/{repo}/badges/{branch}/pipeline.svg')

    def get_status(self, repo, host, branch):
        badge_result = requests.get(self.get_badge_url(repo,
                                                       host,
                                                       branch=branch))

        if badge_result.status_code == 404:
            return Status.UNKNOWN
        elif badge_result.status_code != 200:
            return Status.UNDETERMINED

        return self.status_from_badge_svg(badge_result.text)
