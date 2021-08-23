## This repository can be used to reproduce results from our paper [Towards Prioritizing GitHub Issues](https://dl.acm.org/doi/abs/10.1145/3385032.3385052)

### Setting up python environment

```
python3 -m venv venv
pip install -r requirements.txt
source venv/bin/activate
```

### Section 5.1: Dataset

The dataset of 1500 closed and 1500 open issues pulled from Tensorflow repository is available under `final/data` folder in pickle file format.

Reading the issue pickle files:
a. `tf_issues.pickle`
b. `tf_closed_issues.pickle`

```python
f = open('data/tf_closed_issues.pickle', 'rb')
issues = pickle.load(f)
f.close()

# issues is a JSON List consisting of `json` objects with the following keys (one per issue). 

# number
# id
# created_at
# state
# author_association
# title
# body
# comments
# timeline_url
# closed_at
# labels
# assignees
```

Reading the issue states pickle files:
a. `tf_issue_states.pickle`
b. `tf_closed_issue_states.pickle`

```python
f = open('data/tf_closed_issue_states.pickle', 'rb')
all_states = pickle.load(f)
f.close()

# Reads a list of State objects as defined in final/State.py
```

### Section 5.2 : Hotness of the issue

The following script reads dataset from the pickles, evaluates and prints the Pearson correlation coefficient and the Spearman correlation coefficient as descibed in Section 5.2 of the paper.

```
# within final folder
python hotness.py
```

### Section 5.3 : Lifetime of te issue

The following script measures classification accuracy of different classifiers on the task of predicting closing date for issues as presented in Table 5 of the paper.

```
# within final folder
python predict_close_date.py
```

### Plot for issue lifetimes

The following script generates the graph for issue lifetimes vs number of issues as presented in Figure-3 of the paper.

```
# within final folder
python chart_close_dates.py
```

### Generating issue categories

The following scripts performs LDA on the whole corpus of issues and prints identified topics. It also prints topics and their associated scores for some sample issues.

```
# within final folder
python lda.py
```

### Retrieving more data

Scripts used to scrape the dataset can be found under `final/data_retrieval`. Please add your GitHub authentication token and specify the number of pages to scrape in `final/data_retrieval/Config.py`. 100 issues are scraped per page. The default repository is set to `tensorflow` and issue state is set to `closed` which can also be changed from `Config.py`. Then run,

```
# within final folder
python data_retrieval/Timeline.py 

# This generates pickle files for issues and issue timelines. 
````


