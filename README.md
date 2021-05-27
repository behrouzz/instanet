**Author:** [Behrouz Safari](https://behrouzz.github.io/)<br/>
**License:** [MIT](https://opensource.org/licenses/MIT)<br/>

# instanet
*A python package for analysing Instagram network*


## Installation

Install the latest version of *instanet* from [PyPI](https://pypi.org/project/instanet/):

    pip install instanet

Requirements are *requests*, *networkx* and *matplotlib*.


## Quick start

```python
from instanet import Instagram

ins = Instagram(USERNAME, PASSWORD)
ins.login()
ins.save_friends(['friend1', 'friend2', 'friend3', 'friend4', 'friend5'])
ins.graph()
```