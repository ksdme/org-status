import responses

from org_status.status_providers.appveyor import AppVeyorStatus
from org_status.status_providers import Status
from org_status.status_providers.travis import TravisBuildStatus


def retrieve_file_from_test_data(filename):
    try:
        with open(f'tests/data/{filename}', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None


@responses.activate
def test_travis_get_status_provider_status():
    up_json = {'status': {'description': 'all systems operational'}}
    down_json = {'status': {'description': 'not really working'}}

    responses.add(responses.GET,
                  TravisBuildStatus.TravisStatusUrl,
                  json=up_json)

    responses.add(responses.GET,
                  TravisBuildStatus.TravisStatusUrl,
                  json=down_json)

    responses.add(responses.GET,
                  TravisBuildStatus.TravisStatusUrl,
                  status=500)

    assert TravisBuildStatus.get_status_provider_status() is True
    assert TravisBuildStatus.get_status_provider_status() is False
    assert TravisBuildStatus.get_status_provider_status() is None


@responses.activate
def test_travis_get_status():
    travis_check_url = ('https://api.travis-ci.org/coala'
                        '/coala-bears.svg?branch=master')
    responses.add(responses.GET,
                  travis_check_url,
                  status=200,
                  body=retrieve_file_from_test_data('failing.svg'))

    responses.add(responses.GET,
                  travis_check_url,
                  status=200,
                  body=retrieve_file_from_test_data('passing.svg'))

    responses.add(responses.GET,
                  travis_check_url,
                  status=500)

    assert TravisBuildStatus('coala').get_status('coala-bears',
                                                 'github',
                                                 'master') == Status.FAILING

    assert TravisBuildStatus('coala').get_status('coala-bears',
                                                 'github',
                                                 'master') == Status.PASSING

    assert TravisBuildStatus('coala').get_status('coala-bears',
                                                 'github',
                                                 'master') == (Status.
                                                               UNDETERMINED)


@responses.activate
def test_appveyor_get_status():
    appveyor_status_url = ('https://ci.appveyor.com/api/projects/status/'
                           'github/coala/coala-bears?branch=master&svg=true')
    responses.add(responses.GET,
                  appveyor_status_url,
                  status=200,
                  body=retrieve_file_from_test_data('passing.svg'))

    responses.add(responses.GET,
                  appveyor_status_url,
                  status=500)

    responses.add(responses.GET,
                  appveyor_status_url,
                  status=200,
                  body=retrieve_file_from_test_data('failing.svg'))

    assert AppVeyorStatus('coala').get_status('coala-bears',
                                              'github',
                                              'master') == Status.PASSING

    assert AppVeyorStatus('coala').get_status('coala-bears',
                                              'github',
                                              'master') == Status.UNDETERMINED

    assert AppVeyorStatus('coala').get_status('coala-bears',
                                              'github',
                                              'master') == Status.FAILING
