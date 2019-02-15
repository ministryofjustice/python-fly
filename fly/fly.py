import json
import os
import platform
import subprocess

import requests


DEFAULT_FLY_BIN = '/usr/local/bin/fly'


class Fly:
    def __init__(
        self,
        concourse_url,
        executable=DEFAULT_FLY_BIN,
        target='default'
    ):
        self.concourse_url = concourse_url
        self.executable = executable
        self.target = target

    def get_fly(self):
        if not os.path.isfile(self.executable):
            url = f'{self.concourse_url}/api/v1/cli'
            params = {
                'arch': 'amd64',
                'platform': platform.system().lower()
            }
            response = requests.get(url, params=params, stream=True)
            if response.status_code == 200:
                with open(self.executable, 'wb') as f:
                    for chunk in response:
                        f.write(chunk)
                self.make_file_executable()

    def make_file_executable(self):
        os.chmod(self.executable, 0o755)

    def run(self, cmd, *args):
        return subprocess.run(
            [self.executable, '-t', self.target, cmd, *args],
            stdout=subprocess.PIPE,
            check=True
        )

    def login(self, username, password, team_name):
        self.run(
            'login',
            '-c', self.concourse_url,
            '-u', username,
            '-p', password,
            '-n', team_name
        )

    def get_json(self, item, *args):
        items_json = self.run(
            item,
            *args,
            '--json',
        ).stdout
        return json.loads(items_json)
