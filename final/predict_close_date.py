import pandas as pd
import re
import copy
import numpy as np
import matplotlib.pyplot as plt
from dateutil.parser import parse
import pickle
import numpy as np

f = open('data/tf_closed_issues.pickle', 'rb')
issues = pickle.load(f)
f.close()

def transformDate(t, t0):
    t = parse(t)
    t0 = parse(t0)
    return (t - t0).total_seconds()/ (60.0 * 60.0 * 24)

def auth_assoc(s):
    if(s=="OWNER"):
        return 4
    elif(s=="MEMBER"):
        return 3
    elif(s=="CONTRIBUTOR"):
        return 2
    elif(s=="NONE"):
        return 1
    else:
        return 0

def classify_closeTime(i):
    if i < 3.0:
        return 0
    elif i >= 3.0 and i < 8.0:
        return 1
    elif i >= 8.0 and i < 15.0:
        return 2
    elif i >= 15.0 and i < 28:
        return 3
    else:
        return 4

X = []
y = []

for issue in issues:
    x = [len(issue['labels']), len(issue['assignees']), \
        auth_assoc(issue['author_association'])]
    X.append(x)
    t = transformDate(issue['closed_at'], issue['created_at'])
    y.append(classify_closeTime(t))

X = np.array(X)
y = np.array(y)

from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from sklearn import metrics
# X_train, X_test, y_train, y_test = train_test_split(X,y,train_size=0.9, random_state=1)

sss = StratifiedShuffleSplit(n_splits=2, test_size=0.25, random_state=0)
sss.get_n_splits(X, y)
for train_index, test_index in sss.split(X, y):
    print(" --- Results for new split --- ")
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    from sklearn.neighbors import KNeighborsClassifier #max at n_neihbors = 5 mean =48.989%
    knn = KNeighborsClassifier(n_neighbors=1)
    from sklearn.model_selection import GridSearchCV
    k_range = [i for i in range(1,31)]
    param_grid = dict(n_neighbors = k_range)
    grid = GridSearchCV(knn,param_grid,cv=10,scoring="accuracy")
    grid.fit(X,y)
    y_pred = grid.predict(X_test)
    print('KNN', metrics.accuracy_score(y_test, y_pred))
    print(grid.best_estimator_)

    from sklearn.linear_model import LogisticRegression#52.8846%
    logreg = LogisticRegression()
    logreg.fit(X_train,y_train)
    y_pred = logreg.predict(X_test)
    print('Logistic Regression:', metrics.accuracy_score(y_test, y_pred))


    from sklearn.tree import DecisionTreeClassifier #54.807%
    tree1 = DecisionTreeClassifier(max_depth=5)
    tree1.fit(X_train,y_train)
    y_pred = tree1.predict(X_test)
    print('Decision Tree:', metrics.accuracy_score(y_test, y_pred))


    from sklearn.ensemble import RandomForestClassifier#49- 51%
    rnd_forest = RandomForestClassifier()
    rnd_forest.fit(X_train,y_train)
    y_pred = rnd_forest.predict(X_test)
    print('Random Forest:', metrics.accuracy_score(y_test, y_pred))


    from sklearn.svm import SVC #54.807%
    svmCls = SVC(probability=True)
    svmCls.fit(X_train,y_train)
    y_pred = svmCls.predict(X_test)
    print('SVM:', metrics.accuracy_score(y_test, y_pred))


    # from sklearn.ensemble import VotingClassifier#55.769%
    # rnd_forest = RandomForestClassifier()
    # logreg = LogisticRegression()
    # tree1 = DecisionTreeClassifier(max_depth=2)
    # svmCls = SVC(probability=True)
    # es =[("rf",rnd_forest),("lr", logreg),("dt",tree1),("svc",svmCls)]
    # voting_cls = VotingClassifier(estimators=es,voting="soft")
    # voting_cls.fit(X_train,y_train)
    # y_pred = voting_cls.predict(X_test)
    # print(metrics.accuracy_score(y_test,y_pred))

    from sklearn.metrics import plot_confusion_matrix
    # target_names = {
    #     0: '0 to 3',
    #     1: '3 to 8',
    #     2: '8 to 15',
    #     3: '15 to 28',
    #     4: '>28'
    # }
    # plot_confusion_matrix(rnd_forest, X_test, y_test)
