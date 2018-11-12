from os import environ, path
from multiprocessing.dummy import Pool
from argparse import ArgumentParser

from termcolor import colored

from org_status.status_providers import Status, get_supported_status_providers
from org_status.org_hosts import get_all_supported_hosts
from org_status.encoders import get_all_supported_encoders


def get_host_token(host_name):
    return environ['{}_TOKEN'.format(host_name.upper())]


def get_status_provider_statuses():
    for provider in get_supported_status_providers():
        try:
            yield (provider, provider.get_status_provider_status())
        except NotImplementedError:
            yield (provider, None)


def generate_fetch_jobs(org_strings):
    for org_string in org_strings:
        host, sym, org = org_string.strip().partition(':')
        host = host.lower()

        if sym == '':
            host, org = '', host

        if org == '':
            raise ValueError('org name invalid')

        if host != '':
            for supported_host in get_all_supported_hosts():
                if host == supported_host.HostName:
                    yield (supported_host, org)
                    raise StopIteration
        else:
            for available_host in get_all_supported_hosts():
                yield (available_host, org)


def aggregate_org_status(org_host, threads=2):
    with Pool(processes=threads) as pool:
        return pool.map(org_host.process_repository, org_host.repositories)


def present_status(statuses, no_color):
    color = (lambda l, *_: l) if no_color else colored
    r_pass, r_fail, r_unknown, r_error = 0, 0, 0, 0

    for status in statuses:
        repo_status = status.repo_status or Status.UNDETERMINED
        status_text = repo_status.value

        if repo_status == Status.PASSING:
            status_text = color(status_text, 'green')
            r_pass += 1
        elif repo_status == Status.FAILING:
            status_text = color(status_text, 'red')
            r_fail += 1
        elif repo_status == Status.ERROR:
            status_text = color(status_text, 'magenta')
            r_error += 1
        elif repo_status in [Status.UNKNOWN, Status.UNDETERMINED]:
            r_unknown += 1
            continue

        print('{repo}: {status}'.format(
            repo=status.repo_url, status=status_text))

    print('{} Passing, {} Failing, {} Error, {} Unknown '
          'of {} Repositories'.format(
            r_pass, r_fail, r_error, r_unknown, len(statuses)))


def get_argument_parser():
    parser = ArgumentParser()
    parser.add_argument('orgs', nargs='*', help='host:org')
    parser.add_argument('--threads', type=int, default=2)
    parser.add_argument('--no-color', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--hosts-only', '-o', action='store_true')
    parser.add_argument('--skip-host-checks', action='store_true')
    parser.add_argument('--export-repos', type=str)
    parser.add_argument('--format', type=str, default='gitman')
    parser.add_argument('--check-providers-only', action='store_true')

    return parser


def encode_repo_list(repo_data, encoder_name, styled):
    encoders = get_all_supported_encoders()
    encoded_repo_list = None

    for encoder in encoders:
        if encoder.NAME == encoder_name:
            try:
                encoded_repo_list = encoder().convert_repo_list_to_format(
                    repo_data)
            except NotImplementedError:
                print(styled(
                        f'{encoder_name} does not support exporting results',
                        'red'))
        else:
            print(styled(f'unknown export format {encoder_name}', 'red'))

    return encoded_repo_list


def write_data_to_file(encoded_data, filename, styled, verbose):
    if encoded_data is not None:
        try:
            with open(filename, 'w') as file:
                file.write(encoded_data)
                verbose(f'exported repo list as {filename}')
        except FileNotFoundError:
            print(styled(f'unable to find file {filename}', 'red'))


def main():
    parser = get_argument_parser()
    args = parser.parse_args()

    styled = (lambda l, *_: l) if args.no_color else colored
    verbose = print if args.verbose else (lambda *_: None)

    hosts_only_print = print if args.hosts_only else verbose

    if args.check_providers_only:
        for provider, status in get_status_provider_statuses():
            if provider is not None:
                print(styled(f'{provider.NAME}: {str(status).lower()}',
                             'green' if status else 'red'))
            else:
                print(styled(
                    f'{provider.NAME} does not support status check', 'red'))

        return

    if len(args.orgs) == 0 and args.hosts_only:
        args.orgs = ['coala']
    elif len(args.orgs) == 0:
        print(styled('no organizations to check', 'red'))
        return

    all_repositories = []

    for Host, org in generate_fetch_jobs(args.orgs):
        token = None

        if not args.skip_host_checks:
            try:
                if not Host.get_host_status():
                    print(styled(f'{Host.HostName} is currently down', 'red'))
                    continue
                else:
                    hosts_only_print(f'{Host.HostName} is up')
            except NotImplementedError:
                verbose(
                    f'{Host.HostName} does not support checking host status')

        if args.hosts_only and args.skip_host_checks:
            verbose('nothing to do')
            return
        elif args.hosts_only:
            continue

        if (args.verbose):
            print(f'processing org {Host.HostName}:{org}')

        try:
            token = get_host_token(Host.HostName)
        except KeyError as exp:
            clean_exp = str(exp).replace("'", '')

            if clean_exp.endswith('TOKEN'):
                token_type = clean_exp.replace('_TOKEN', '').title()

                text = (f'Lookup requires an access token from {token_type} '
                        f'with permissions to this organization. Please set '
                        f'an environment variable named {clean_exp}.')

                print(styled(text, 'red'))

                continue

            raise exp

        org_host = Host(token, org, verbose=args.verbose)

        if args.export_repos:
            all_repositories += org_host.repositories
            continue

        org_status = aggregate_org_status(org_host, threads=args.threads)
        present_status(org_status, args.no_color)

    if args.export_repos:
        export_data = encode_repo_list(all_repositories, args.format, styled)
        export_file = path.abspath(args.export_repos)

        if len(all_repositories) > 0:
            write_data_to_file(export_data, export_file, styled, verbose)
        else:
            verbose(f'exporting failed {export_file}')
