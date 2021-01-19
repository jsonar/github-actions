import re


def list_issue_numbers(line, keyword):
    issue_numbers = []
    word_list = line.split()
    for i, word in enumerate(word_list):
        if word == keyword:
            if len(word_list) <= i + 1:
                break
            issue = Issue(word_list[i + 1])
            if issue.number:
                issue_numbers.append(issue.number)

    return issue_numbers


class Issue:
    pattern = r'^#([0-9]*)|https:\/\/github\.com\/.*\/.*\/issues\/([0-9]*)'

    def __init__(self, word):
        self.word = word

    @property
    def number(self):
        match = re.search(self.pattern, self.word)

        if match is None:
            return

        for group in match.groups():
            if group:
                return group
