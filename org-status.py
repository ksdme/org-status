from os import environ
from multiprocessing import Pool
from argparse import ArgumentParser

import requests
from termcolor import colored
from IGitt.GitHub.GitHub import GitHub, GitHubToken
from IGitt.GitHub.GitHubOrganization import GitHubOrganization

error = 'error'
unknown = 'unknown'
failing = 'failing'
passing = 'passing'

def process_travis_result(html):
  html = html.lower()

  for status in [passing, failing, unknown, error]:
    if status in html:
      return status    

def get_travis_status(repo, branch='master'):
  url = 'https://api.travis-ci.org/coala/{repo}.svg?branch={branch}'.format(
          repo=repo, branch=branch)

  svg_result = requests.get(url)
  svg = svg_result.text

  return process_travis_result(svg)

def process_repo(repo):
  repo_name = repo.web_url.split('/')[-1]
  return (repo.web_url, get_travis_status(repo_name))

def get_org_repo_status(token, org_name):
  gh_org = GitHubOrganization(token, org_name)

  with Pool(processes=8) as pool:
    return pool.map(process_repo, gh_org.repositories)

if __name__ == '__main__':
  token = GitHubToken(environ['GITHUB_TOKEN'])

  parser = ArgumentParser()
  parser.add_argument('org')
  parser.add_argument('--no-color', action='store_true')

  args = parser.parse_args()
  org = args.org

  color = (lambda l, *_: l) if args.no_color else colored
  total, r_pass, r_fail, r_unknown, r_error = 0, 0, 0, 0, 0

  for repo, status in get_org_repo_status(token, org):
    total += 1

    if status == passing:
      status = color(status, 'green')
      r_pass += 1
    elif status == failing:
      status = color(status, 'red')
      r_fail += 1
    elif status == error:
      status = color(status, 'magenta')
      r_error += 1
    elif status == unknown:
      r_unknown += 1
      continue

    print('{repo}: {status}'.format(repo=repo, status=status))

  print('{} Passing, {} Failing, {} Error, {} Unknown'
        'of {} Repositories'.format(
            r_pass, r_fail, r_error, r_unknown, total))
