class RepoListEncoder:
    NAME = None

    def convert_repo_list_to_format(self, repos):
        raise NotImplementedError()


def get_all_supported_encoders():
    from org_status.encoders.gitman import GitManEncoder

    return (
        GitManEncoder,
    )
