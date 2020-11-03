import sys
from github import GitHubClient

ARGS_NUMBER = 3


def main():
    if len(sys.argv) != ARGS_NUMBER:
        print(f'Usage: {sys.argv[0]} USERNAME ACCESS_TOKEN')
        return

    with GitHubClient(sys.argv[1], sys.argv[2]) as client:
        for repo in client.get_public_repos():
            print(repo['name'])


if __name__ == '__main__':
    main()
