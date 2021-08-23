## This repository can be used to reproduce results from our paper [Towards Prioritizing GitHub Issues](https://dl.acm.org/doi/abs/10.1145/3385032.3385052)

### Dataset

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

Scripts used to scrape the dataset can be found under `final/data_retrieval`. Please add your GitHub authentication token and specify the number of pages to scrape in `final/data_retrieval/Config.py`. 100 issues are scraped per page. The default repository is set to `tensorflow` and issue state is set to `closed` which can also be changed from `Config.py`. 

```
python final/data_retrieval/Timeline.py 

# This generate pickle files for issues and issue timelines. 
````
