import os

import click

from client import Client


@click.group()
@click.pass_context
def main(context):
    """Entry point for various github queries"""
    context.ensure_object(dict)

    client = build_client()
    context.obj['client'] = client


def build_client():
    token = os.environ['GITHUB_TOKEN']
    return Client(token)


@main.command()
@click.option('--issue-id', required=True, type=int, help='the issue whose project is to be retrieved')
@click.pass_context
def project(context, issue_id):
    """Retrieve project id for given issue"""
    client = context.obj['client']
    events = client.request(method='GET', url=f'repos/{os.environ["GITHUB_REPOSITORY"]}/issues/{issue_id}/events')
    added_to_project_events = filter(lambda event: event['event'] == 'added_to_project', events)
    latest_event = max(added_to_project_events, key=lambda event: event['created_at'])
    print(latest_event['project_card']['id'])


if __name__ == '__main__':
    main(obj={})
