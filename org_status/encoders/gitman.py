import yaml
from giturlparse import parse

from org_status.encoders import RepoListEncoder


class GitManEncoder(RepoListEncoder):
    NAME = 'gitman'

    def convert_repo_list_to_format(self, repos):
        yml_data = {'sources': []}

        for repo in repos:
            name = parse(repo.web_url).repo
            yml_data['sources'].append({'name': name,
                                        'repo': repo.web_url,
                                        'rev': 'master'})

        return yaml.dump(yml_data, default_flow_style=False)
