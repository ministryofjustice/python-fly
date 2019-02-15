import json
from unittest import TestCase, mock

from fly import Fly


def patch_subprocess(return_value=None):
    def wraps(fn):
        @mock.patch('subprocess.run')
        @mock.patch('fly.Fly._get_fly')
        def test(self, get_fly_mock, run_mock):
            stdout_mock = mock.Mock()
            attrs = {'stdout': return_value}
            stdout_mock.configure_mock(**attrs)
            run_mock.return_value = stdout_mock
            return fn(self, run_mock)
        return test
    return wraps


class TestCommandsRun(TestCase):
    def setUp(self):
        self.fly = Fly(
            concourse_url='http://127.0.0.1:8080'
        )

    @patch_subprocess()
    def test_login(self, run_mock):
        self.fly.login(
            username='admin', password='admin', team_name='main')
        self.assertTrue(run_mock.called)
        run_mock.assert_called_with([
            '/usr/local/bin/fly',
            '-t', 'default',
            'login',
            '-c', 'http://127.0.0.1:8080',
            '-u', 'admin',
            '-p', 'admin',
            '-n', 'main'
        ], check=True, stdout=-1)

    @patch_subprocess(
        json.dumps([
            {
                'id': 1, 'name':
                'hello-world',
                'paused': False,
                'public': False,
                'team_name': 'main'
            }
        ])
    )
    def test_get_json(self, run_mock):
        pipelines = self.fly.get_json('pipelines')
        self.assertTrue(run_mock.called)
        run_mock.assert_called_with([
            '/usr/local/bin/fly',
            '-t', 'default',
            'pipelines',
            '--json'
        ], check=True, stdout=-1)
        self.assertListEqual(pipelines, [
            {
                'id': 1,
                'name': 'hello-world',
                'paused': False,
                'public': False,
                'team_name': 'main'
            }
        ])
