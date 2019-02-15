import json
import os
import subprocess

import requests


class Fly:
    def __init__(
            self, concourse_url, executable='/usr/local/bin/fly',
            platform='darwin', target='default'
    ):
        self.concourse_url = concourse_url
        self.executable = executable
        self.platform = platform
        self.target = target

        if not os.path.isfile(self.executable):
            self._get_fly()

    def _get_fly(self):
        url = f'{self.concourse_url}/api/v1/cli?arch=amd64&platform=' \
            f'{self.platform}'
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(self.executable, 'wb') as f:
                for chunk in response:
                    f.write(chunk)
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
        print(items_json)
        return json.loads(items_json)
