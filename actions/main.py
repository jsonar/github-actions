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
    """Retrieve project card id for given issue"""
    response = Client().request('project.graphql', {'issue_number': issue_id})
    cards = response['data']['repository']['issue']['projectCards']['nodes']
    click.echo(max(cards, key=lambda card: card['createdAt'])['databaseId'])


@main.command()
@click.option('--pr', required=True, type=int, help='The pull request to parse')
@click.option('--keyword', type=str, default='resolves', help='Prefix for ')
def issues(pr, keyword):
    client = Client()
    pull_request_data = client.request('comments.graphql', {'pull_request': pr})['data']['repository']['pullRequest']
    comments = [node['bodyText'] for node in pull_request_data['comments']['nodes']]
    comments.append(pull_request_data['bodyText'])
    issue_numbers = set()
    for comment in comments:
        issue_numbers.update(list_issue_numbers(comment, keyword))
    click.echo(' '.join(issue_numbers))


if __name__ == '__main__':
    main(obj={})
