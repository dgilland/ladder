```
 _           _     _
| |         | |   | |
| | __ _  __| | __| | ___ _ __
| |/ _` |/ _` |/ _` |/ _ \ '__|
| | (_| | (_| | (_| |  __/ |
|_|\__,_|\__,_|\__,_|\___|_|

```

[![Package Version](https://pypip.in/v/ladder/badge.png?v=0.1.0)](https://pypi.python.org/pypi/ladder/)
[![Build Status](https://travis-ci.org/dgilland/ladder.png?branch=master)](https://travis-ci.org/dgilland/ladder)
[![Coverage Status](https://coveralls.io/repos/dgilland/ladder/badge.png?branch=master)](https://coveralls.io/r/dgilland/ladder)
[![License](https://pypip.in/license/ladder/badge.png)](https://pypi.python.org/pypi/ladder/)

HTTP client wrapper with URL generation via object notation and argument passing.

Inspired by [hammock] but without the [requests] dependency (you provide that yourself if you want it).

But why use `ladder` instead of `hammock`?

- Python 3 compatibility!
- No `requests` dependency. If your using `hammock` then you probably already want to use `requests`. But for those of you who are using another type of HTTP client, then `ladder` can be your `hammock`.
- Since there's no `requests` dependency, you can generate URLs using `ladder.URL` without having an HTTP client.
- Inline handling of query string parameters. `hammock` requires that query parameters be passed into the `requests` method call (e.g. `Hammock(...).GET(params={...}`). But with `ladder.API`, you can provide those via keyword arguments at any time during URL generation (e.g. `API(...)(sort='stars').GET()`) or you can stick with `hammock`'s style (`API(...).GET(params={...}`).
- You can force the HTTP method functions to be lowercase instead of UPPERCASE, i.e., `API(...).GET()` or `API(..., upper_methods=False).get()`.

Beyond that the differences between `ladder` and `hammock` are under the hood.


## Requirements

### Compatibility

- Python 2.6
- Python 2.7
- Python 3.2
- Python 3.3
- Python 3.4

### Dependencies

None. (yay!)


## Installation

```python
pip install ladder
```

## Overview

`ladder` has two main classes:

- `ladder.URL`: Utility class for generating URLs via objection notation and argument passing.
- `ladder.Ladder`: HTTP client wrapper which uses `URL` to generate URLs that can be passed to the client when making HTTP method calls (e.g. `get`, `post`, etc).

### URL

Ever wanted to generate URLs using object notation? Well now you can:

```python
from ladder import URL

github = URL('https://api.github.com')
print(github)
# https://api.github.com

search = github.search
print(search)
# https://api.github.com/search

repositories = search.repositories(q='ladder', sort='stars')
print(repositories)
# https://api.github.com/search/repositories?q=ladder&sort=starts&order=desc
```

Don't want to use object notation? You don't have to:

```python
URL('https://api.github.com')('search')('repositories')(q='ladder')
# or all in one
URL('https://api.github.com')('search', 'repositories', q='ladder')
```

Mix-and-match:

```python
URL('https://api.github.com').search('repositories', q='ladder')
```

You can even pass in URL paths as a list:

```python
URL('https://api.github.com')(['search', 'repositories'], q='ladder')
```

And lists of lists (because `URL` supports flattening):

```python
URL('https://api.github.com')([['search', ['repositories']]], q='ladder')
```

Ensure a slash comes last:

```python
print(URL('/').search)
# /search

print(URL('/', append_slash=True).search)
# /search/
```

Don't initialize `URL`:

```python
print(URL()('https://api.github.com').search)
# https://api.github.com/search
```

Create partial URL paths:

```python
print(URL('/path/to/resource').subresource)
# /path/to/resource/subresource
```

Convert `URL` to string:

```python
url = str(URL('/foo/bar/baz'))
```

Concatenate using `+` and `/` (because, hey, why not!):

```python
start = '/start/of/path'
middle = URL('middle')
end = '/end/of/path'

# supports both URL and string concatenation

URL(start) + middle + URL(end)
URL(start) + middle + end
start + middle + URL(end)

URL(start) / middle / URL(end)
URL(start) / middle / end
start / middle / URL(end)
```

### Ladder

Do what `URL` does but make an HTTP request at the end (_provided you give it a client_)! Now we're really trying to be like [hammock].

After installing [requests]:

```python
import requests
from ladder import Ladder

# If you need to configure your requests session,
# better do it before passing it into Ladder().
# Ladder assumes your client is ready-to-go and doesn't
# provide an easy way to configure it once it's passed in.
Rung = Ladder(requests.session())

github = Rung('https://api.github.com')
results = github.search.repositories(q='ladder').GET().json()

api = Rung('https://api.example.com')
data = {}
api.users.POST(data).json()
api.users(1).PUT(data).json()
api.users(1).DELETE().json()
api.users.HEAD()
api.users.OPTIONS()
```

Don't like having to use UPPERCASE HTTP METHODS? No problem! `Ladder` has you covered:

```python
github = Ladder(requests.session(), 'https://api.github.com', uppercase_methods=False)
results = github.search.repositories(q='ladder').get().json()
```

Just remember you'll need to pass a `string` for any of the lowercase HTTP methods that are in the URL path:

```python
api = Ladder(requests.session(), '/api/', uppercase_methods=False)
api.item('get').details.get()
```

[hammock]: https://github.com/kadirpekel/hammock
[requests]: https://github.com/kennethreitz/requests
