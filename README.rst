Snakes on a plane
=================

A python package to run concourse fly

Useage
======

..  code:: python

    from fly import Fly
    fly = Fly(
        concourse_url='http://127.0.0.1:8080'
    )
    fly.get_fly()
    fly.login(username='admin', password='admin', team_name='main')
    fly.get_json('pipelines')
    fly.run(
        'set-pipeline',
        '-p', 'concourse-build',
        '-c', '/path/to/resource/pipeline.yaml',
        '-v', 'app-name=app_name',
        '-v', 'github-org=github-org',
        '-v', 'github-repo=https://github.com/ministryofjustice/concourse-build',
        '-n'
    )

Tests
=====

..  code:: bash

    python -m unittest tests.test_commands_run -v
