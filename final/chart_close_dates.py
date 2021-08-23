import pickle
from matplotlib import pyplot as plt
from dateutil.parser import parse

f = open('data/tf_closed_issues.pickle', 'rb')
issues = pickle.load(f)
f.close()

def transformDate(t, t0):
    t = parse(t)
    t0 = parse(t0)
    return (t - t0).total_seconds()/ (60.0 * 60.0 * 24)

def mapAuthorAssoc(a):
    if a == 'MEMBER' or a == 'OWNER':
        return 2
    elif a == 'CONTRIBUTOR':
        return 1
    else:
        return 0

X = []
y = []

for issue in issues:
    x = [len(issue['labels']), len(issue['assignees']), \
        mapAuthorAssoc(issue['author_association'])]
    X.append(x)
    t = transformDate(issue['closed_at'], issue['created_at'])
    y.append(t)

max_t = int(max(y))
min_t = int(min(y))

plt.hist(y, max_t - min_t + 1, histtype = 'step', \
    label = 'number of points', color = 'r')
plt.xlabel('days')
plt.ylabel('number')
plt.legend()
# plt.show()
plt.savefig('data.png')