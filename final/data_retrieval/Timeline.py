from Config import *
import requests
import json
from Retrieve import retrieve, retrieve2
from State import State
from dateutil.parser import parse
import copy
import pickle

url = 'https://api.github.com/repos/' + org_name + '/' + repo_name + \
    '/issues'
issues = retrieve2(url)

print('Finished retrieving issues. Total issues fetched', len(issues))

all_states = []
for n, issue in enumerate(issues):
    issue_no = issue['number']
    authorAssoc = issue['author_association']
    url = issue['timeline_url']
    print('Fetching timeline for issue', n+1, '/', len(issues))
    event_list = retrieve(url)
    relevant_types = ['commented', 'assigned', 'unassigned', 'labeled', \
        'unlabeled']
    prev_state = State(issue_no, authorAssoc)
    for i in range(len(event_list)-1):
        event = event_list[i]
        event_type = event['event']
        if event_type not in relevant_types:
            continue
        event_time = event['created_at']
        new_state = copy.deepcopy(prev_state)
        new_state.currentEventTime = event_time
        if event_type == 'commented':
            new_state.addComment(event_time)
        elif event_type == 'assigned':
            new_state.addAssignee(event_time, event['assignee']['id'])
        elif event_type == 'unassigned':
            new_state.removeAssignee(event['assignee']['id'])
        elif event_type == 'labeled':
            new_state.addLabel(event_time, event['label']['name'])
        else:
            new_state.removeLabel(event['label']['name'])
        if 'created_at' in event_list[i+1]:
            new_state.eventTime = event_list[i+1]['created_at']
            all_states.append(new_state)
        prev_state = new_state

f = open('tf_closed_issues.pickle', 'wb')
pickle.dump(issues, f)
f.close()

f = open('tf_closed_issue_states.pickle', 'wb')
pickle.dump(all_states, f)
f.close()
