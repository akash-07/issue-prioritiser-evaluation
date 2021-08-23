
class State:

    def __init__(self, issue_id, authorAssoc):
        self.issue_id = issue_id
        self.assignees = [] # (assignee_id, ts)
        self.comments = []
        self.labels = []    # (label_name, ts)
        self.authorAssoc = 0
        self.eventTime = None
        if(authorAssoc == 'MEMBER' or authorAssoc == 'OWNER'):
            self.authorAssoc = 0
        elif(authorAssoc == 'CONTRIBUTOR'):
            self.authorAssoc = 1

    def addAssignee(self, ts, assignee_id):
        self.assignees.append((assignee_id, ts))

    def getAssignees(self):
        return self.assignees

    def removeAssignee(self, assignee_id):
        self.assignees = [tp for tp in self.assignees if tp[0] != assignee_id]

    def addComment(self, ts):
        self.comments.append(ts)

    def getComments(self):
        return self.comments

    def removeComment(self, ts):
        self.comments.remove(ts)

    def addLabel(self, ts, label_name):
        self.labels.append((label_name, ts))

    def getLabels(self):
        return self.labels

    def removeLabel(self, label_name):
        self.labels = [tp for tp in self.labels if tp[0] != label_name]

    def __repr__(self):
        state_string = \
            'Issue Id: ' + str(self.issue_id) + '\nFeatures:\n' + \
            '1) Assignees: ' + str(len(self.assignees)) + '\n' + \
            '2) Comments: ' + str(len(self.comments)) + '\n' + \
            '3) Labels: ' + str(len(self.labels)) + '\n' + \
            '4) Author association: ' + str(self.authorAssoc) + '\n' + \
            'Event Time: ' + str(self.eventTime) + '\n'
        return state_string
