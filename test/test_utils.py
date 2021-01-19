import pytest

from utils import list_issue_numbers


def test_list_issue_numbers_short_link():
    line = 'resolves #200'
    assert ['200'] == list_issue_numbers(line, 'resolves')


def test_list_issue_numbers_simple_link():
    line = 'resolves https://github.com/jsonar/audit-policy/issues/240'
    assert ['240'] == list_issue_numbers(line, 'resolves')


def test_list_issue_numbers_keyword_missing():
    line = 'foo #200'
    assert [] == list_issue_numbers(line, 'resolves')


def test_list_issue_numbers_no_link():
    line = 'resolves but no link'
    assert [] == list_issue_numbers(line, 'resolves')


def test_list_issue_numbers_keyword_is_last():
    line = 'bla bla resolves'
    assert [] == list_issue_numbers(line, 'resolves')


def test_list_issue_numbers_complicated_sentence():
    line = 'this complicated sentence resolves #200'
    assert ['200'] == list_issue_numbers(line, 'resolves')


def test_list_issue_numbers_multiple_issues():
    line = 'resolves #200 resolves #201'
    assert ['200', '201'] == list_issue_numbers(line, 'resolves')


def test_list_issue_numbers_empty_body():
    line = ''
    assert [] == list_issue_numbers(line, 'resolves')
