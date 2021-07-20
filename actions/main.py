import os

import click

from actions.client import Client
from actions.utils import list_issue_numbers


@click.group()
@click.pass_context
def main(context):
    """Entry point for various github queries"""
    context.ensure_object(dict)


@main.command()
@click.option('--issue-id', required=True, type=int, help='the issue whose project is to be retrieved')
def project(issue_id):
    """Retrieve project id for given issue"""
    events = Client().request(method='GET', url=f'repos/{os.environ["GITHUB_REPOSITORY"]}/issues/{issue_id}/events')
    added_to_project_events = filter(lambda event: event['event'] == 'added_to_project', events)
    latest_event = max(added_to_project_events, key=lambda event: event['created_at'])
    click.echo(latest_event['project_card']['id'])


@main.command()
@click.option('--pr', required=True, type=int, help='The pull request to parse')
@click.option('--keyword', type=str, default='resolves', help='Prefix for ')
def issues(pr, keyword):
    client = Client()
    raw_comments = client.request(method='GET', url=f'repos/{os.environ["GITHUB_REPOSITORY"]}/issues/{pr}/comments')
    comments = [raw_comment['body'] for raw_comment in raw_comments]
    comments.append(client.request(method='GET', url=f'repos/{os.environ["GITHUB_REPOSITORY"]}/pulls/{pr}')['body'])
    issue_numbers = set()
    for comment in comments:
        issue_numbers.update(list_issue_numbers(comment, keyword))
    click.echo(" ".join(issue_numbers))


if __name__ == '__main__':
    main(obj={})
