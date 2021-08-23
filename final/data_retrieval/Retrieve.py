import Config
import requests
import json
import re

def retrieve(url, page = 1):
    if(page > Config.max_pages):
        return []
    print('Retrieving:', url)
    r = requests.get(url, params = Config.params, headers = Config.headers)
    headers = r.headers
    data = r.content
    js = json.loads(data)
    links = re.findall(r'<(.+?)>', headers.get('Link', ''))
    pointers = re.findall(r'rel=\"(\S+)\"', headers.get('Link', ''))
    limit = headers['X-RateLimit-Remaining']
    if limit:
        print('Limit Remaining:', limit)
        if(int(limit) == 0):
            return
    for i in range(0, len(pointers)):
        if(pointers[i] == 'next'):
            url = links[i]
            return js + retrieve(url, page + 1)
    return js

def retrieve2(url, page = 1):
    if(page > Config.max_pages):
        return []
    print('Retrieving:', url)
    r = requests.get(url, params = Config.params, headers = Config.headers)
    headers = r.headers
    data = r.content
    js = json.loads(data)
    issues = []
    for full_issue in js:
        issue = {}
        print(full_issue['state'])
        issue['number'] = full_issue['number']
        issue['id'] = full_issue['id']
        issue['created_at'] = full_issue['created_at']
        issue['state'] = full_issue['state']
        issue['author_association'] = full_issue['author_association']
        issue['title'] = full_issue['title']
        issue['body'] = full_issue['body']
        issue['comments'] = full_issue['comments']
        issue['timeline_url'] = full_issue['timeline_url']
        if issue['state'] == 'closed':
            issue['closed_at'] = full_issue['closed_at']
        full_labels = full_issue.get('labels', [])
        labels = []
        for full_label in full_labels:
            label = {}
            label['name'] = full_label['name']
            labels.append(label)
        issue['labels'] = labels

        full_assignees = full_issue.get('assignees', [])
        assignees = []
        for full_assignee in full_assignees:
            assignee = {}
            assignee['login'] = full_assignee['login']
            assignee['id'] = full_assignee['id']
        issue['assignees'] = assignees
        issues.append(issue)

    links = re.findall(r'<(.+?)>', headers['Link'])
    pointers = re.findall(r'rel=\"(\S+)\"', headers['Link'])
    limit = headers['X-RateLimit-Remaining']
    if limit:
        print('Limit Remaining:', limit)
        if(int(limit) == 0):
            return
    for i in range(0, len(pointers)):
        if(pointers[i] == 'next'):
            url = links[i]
            return issues + retrieve2(url, page + 1)
    return issues
