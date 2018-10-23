## How it works?
`org-status` uses SVG labels from CI/CD systems to determine build status of all repos under an organization.

- Supported Hosts
  - Github
  - Gitlab

- Supported CI Services
  - Travis
  - Gitlab CI

## Usage

```shell
usage: __main__.py [-h] [--threads THREADS] [--no-color] [--verbose]
                   orgs [orgs ...]

positional arguments:
  orgs               host:org

optional arguments:
  -h, --help         show this help message and exit
  --threads THREADS
  --no-color
  --verbose, -v
```

Git host specific tokens are required to be available as environment variables. Org names should be in the form of `host:org`, if no host is passed then it checks the repo against all available hosts, `:` is optional in case the host is omitted. Organization has to be in scope of access tokens. Use `--no-color` for no colored mode.
