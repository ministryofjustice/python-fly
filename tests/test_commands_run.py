from unittest import TestCase, mock

from fly import Fly


def patch_subprocess(return_value=None):
    def wraps(fn):
        @mock.patch('subprocess.run')
        def test(self, run_mock):
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
            concourse_url='http://localhost:8080'
        )

    @patch_subprocess()
    def test_login(self, run_mock):
        self.fly.login(
            username='username', password='password', team_name='team_name')
        self.assertTrue(run_mock.called)
        run_mock.assert_called_with([
            '/usr/local/bin/fly',
            '-t', 'default',
            'login',
            '-c', 'http://localhost:8080',
            '-u', 'username',
            '-p', 'password',
            '-n', 'team_name'
        ], check=True, stdout=-1)

    @patch_subprocess('[]')
    def test_get_json(self, run_mock):
        pipelines = self.fly.get_json('pipelines')
        self.assertTrue(run_mock.called)
        run_mock.assert_called_with([
            '/usr/local/bin/fly',
            '-t', 'default',
            'pipelines',
            '--json'
        ], check=True, stdout=-1)
        self.assertListEqual(pipelines, [])
