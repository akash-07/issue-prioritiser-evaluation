import pickle
from dateutil.parser import parse
from math import log10, log2
from scipy.stats import pearsonr, spearmanr

f = open('data/tf_closed_issues.pickle', 'rb')
issues1 = pickle.load(f)
f.close()

f = open('data/tf_issues.pickle', 'rb')
issues2 = pickle.load(f)
f.close()

issues = issues1 + issues2

f = open('data/tf_closed_issue_states.pickle', 'rb')
all_states1 = pickle.load(f)
f.close()

f = open('data/tf_issue_states.pickle', 'rb')
all_states2 = pickle.load(f)
f.close()

all_states = all_states1 + all_states2

date_map = {}
for issue in issues:
    date_map[issue['number']] = issue['created_at']

def transformDate(t, t0):
    t = parse(t)
    t0 = parse(t0)
    return (t - t0).total_seconds()/ (60.0 * 60.0)

def transformState(state):
    t = state.eventTime
    state.assignees = [transformDate(t, tp[1]) for tp in state.assignees]
    state.labels = [transformDate(t, tp[1]) for tp in state.labels]
    state.comments = [transformDate(t, cd) for cd in state.comments]
    state.issueCreationDate = transformDate(t, date_map[state.issue_id])
    state.time_elasped = transformDate(t, state.currentEventTime)
    return state

# Evaluates Issue hotness at given state
def evalState(state):
    val = 0.0
    for v in state.assignees:
        val += 1.0/log10(2+v)
    for v in state.labels:
        val += 1.0/log10(2+v)
    for v in state.comments:
        val += 1.0/log2(2+v)
    val += state.authorAssoc/log10(2+state.issueCreationDate)
    return val

formula_vals = list(map(evalState, map(transformState, all_states)))
event_vals = list(map(lambda s: s.time_elasped, all_states))

cleaned_event_vals = []
cleaned_formula_vals = []
for i in range(len(event_vals)):
    if(event_vals[i] != 0):
        cleaned_formula_vals.append(formula_vals[i])
        cleaned_event_vals.append(event_vals[i])

c1, _ = pearsonr(cleaned_formula_vals, cleaned_event_vals)
c2, _ = spearmanr(cleaned_formula_vals, cleaned_event_vals)

print('Pearson coefficient', c1)
print('Spearman coefficient', c2)
