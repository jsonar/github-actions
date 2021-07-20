import os

import pytest
from click.testing import CliRunner

from actions.main import main


@pytest.fixture(scope='module', autouse=True)
def validate_environent():
    assert 'GITHUB_TOKEN' in os.environ, 'This test must be run with the GITHUB_TOKEN env variable'

def test_project():
    os.environ['GITHUB_REPOSITORY'] = 'jsonar/audit-policy'
    runner = CliRunner()
    result = runner.invoke(main, ['project', '--issue-id',  '333'])
    assert result.exit_code == 0
    assert '56044181' in result.output


def test_issues():
    os.environ['GITHUB_REPOSITORY'] = 'jsonar/sage'
    runner = CliRunner()
    result = runner.invoke(main, ['issues', '--pr',  '127'])
    assert result.exit_code == 0
    assert '12' in result.output
