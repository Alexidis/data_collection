import requests
from requests.auth import HTTPDigestAuth
from pathlib import Path
import json
from fake_headers import Headers

header = Headers(headers=True).generate()


def task_1():
    url = 'https://api.github.com/users/Alexidis/repos'
    response = requests.get(url, headers=header)

    my_repos_path = Path.cwd() / 'output/my_repos.json'
    with my_repos_path.open(mode='w', encoding='UTF-8') as my_repos:
        my_repos.write(response.text)


def task_2():
    url = 'https://httpbin.org/digest-auth/auth/user/pass'
    response = requests.get(url, auth=HTTPDigestAuth('user', 'pass'))

    my_repos_path = Path.cwd() / 'output/auth.json'
    with my_repos_path.open(mode='w', encoding='UTF-8') as my_repos:
        json.dump(response.text, my_repos)


if __name__ == '__main__':
    task_1()
    task_2()

