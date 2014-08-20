```
 _           _     _
| |         | |   | |
| | __ _  __| | __| | ___ _ __
| |/ _` |/ _` |/ _` |/ _ \ '__|
| | (_| | (_| | (_| |  __/ |
|_|\__,_|\__,_|\__,_|\___|_|
```

[![Package Version](https://pypip.in/v/ladder/badge.png)](https://pypi.python.org/pypi/ladder/)
[![Build Status](https://travis-ci.org/dgilland/ladder.png?branch=master)](https://travis-ci.org/dgilland/ladder)
[![Coverage Status](https://coveralls.io/repos/dgilland/ladder/badge.png?branch=master)](https://coveralls.io/r/dgilland/ladder)
[![License](https://pypip.in/license/ladder/badge.png)](https://pypi.python.org/pypi/ladder/)

General purpose path generation library with support for URLs, OS paths, delimited paths, and RESTful HTTP client integration.

Inspired by [hammock].


## Background

The need for `ladder` came from working with the [flask] test client during a backend project developing an RESTful API. I wanted an easy way build a test client API that consumed the backend API. I originally started out by having API URLs as class attributes on unittest TestCases which would then get passed to the test client. This worked fine in the beginning, but eventually there was a need for tests to use multiple API endpoints in several places. What I really wanted then was an interface to easily build a test client API which would then be shareable across tests.

With the help of `ladder`, I was able to implement something similiar to the following:

```python
from ladder import API as APIBase


class API(object):
    def __init__(self, client, route_prefix='/api'):
        endpoint = APIBase(client, url=route_prefix, upper_methods=False)

        self.sessions = endpoint('/sessions')
        self.users = endpoint('/users')
        self.products = endpoint('/products')
        self.product_categories = endpoint('/product/categories')


class Client(ClientBase):
    @cached_property
    def api(self):
        return API(self)
```

Which allowed me to use the client in the following manner:

```python
def test_some_api(self):
    # Login.
    self.client.api.sessions(login_data).post()

    # Get all users.
    res = self.client.api.users.get()
    self.assertStatus(res, 200)

    # Get a single user.
    user_id = 1
    res = self.client.api.users(user_id).get()

    # Update a singler user.
    res = self.client.api.users(user_id).post(data=data)
```

For me this made working with the test client easier to manage and more enjoyable.


## Compared to Hammock

Hammock can already do most of what `ladder` does when working with a [requests] based client. So why use `ladder` instead of `hammock` then?

- No `requests` dependency. If you're using `hammock` then you probably already want to use `requests`. But for those of you who are using another type of HTTP client, then `ladder` can be your `hammock`.
- Since there's no `requests` dependency, you can generate URLs using `ladder.URLPath` without having an HTTP client.
- Inline handling of query string parameters. `hammock` requires that query parameters be passed into the `requests` method call (e.g. `Hammock(...).GET(params={...}`). But with `ladder.API`, you can provide those via keyword arguments at any time during URL generation (e.g. `API(...)(sort='stars').GET()`) or you can stick with `hammock`'s style (`API(...).GET(params={...}`). `API` even supports extracting query parameters from string urls.
- You can force the HTTP method functions to be lowercase instead of UPPERCASE, i.e., `API(...).GET()` or `API(..., upper_methods=False).get()`.

Beyond that the differences between `ladder` and `hammock` are under the hood when it comes to being an API client.


## Requirements


### Compatibility

- Python 2.6
- Python 2.7
- Python 3.2
- Python 3.3
- Python 3.4


### Dependencies

None.


## Installation

```python
pip install ladder
```


## Overview

`ladder` has several classes for working with various types of path generation:

- `ladder.URLPath`: Utility class for generating URLs.
- `ladder.OSPath`: Utility class for genearting OS paths.
- `ladder.DelimitedPath`: Utility class for generating delimited paths.
- `ladder.API`: HTTP client wrapper which uses `URLPath` to generate URLs that can be passed to the client when making HTTP method calls (e.g. `GET`, `POST`, etc).


### URLPath

Ever wanted to generate URLs using object notation? Well now you can:

```python
from ladder import URLPath

github = URLPath('https://api.github.com')
print(github)
# https://api.github.com

search = github.search
print(search)
# https://api.github.com/search

repositories = search.repositories(q='ladder', sort='stars')
print(repositories)
# https://api.github.com/search/repositories?q=ladder&sort=stars
```

Don't want to use object notation? You don't have to:

```python
URLPath('https://api.github.com')('users')('dgilland/repos', sort='updated')
# or all in one
URLPath('https://api.github.com', 'users/dgilland', 'repos', sort='updated')
```

Mix-and-match:

```python
URLPath('https://api.github.com').search('repositories', q='ladder')
```

You can even pass in URL paths as a list:

```python
URLPath('https://api.github.com')(['search', 'repositories'], q='ladder')
```

And lists of lists (because `URLPath` supports flattening):

```python
URLPath('https://api.github.com')([['search', ['repositories']]], q='ladder')
```

Need that slash at the end?

```python
print(URLPath('/').search)
# /search
# ...well that isn't what you want

print(URLPath('/', append_slash=True).search)
# /search/
# ...ah, that's better!
```

Create partial URL paths:

```python
print(URLPath('/path/to/resource').subresource)
# /path/to/resource/subresource
```

Supply query string parameters in a variety of ways:

```python
print(URLPath('/path/with?a=1')('query?so=cool', foo='bar')(b=2, c=3)(d=4)(a=2))
# /path/with/query?so=cool&a=1&foo=bar&b=2&c=3&d=4&a=2

print(URLPath('/')(a=[1, 2, 3])(b=4)(b=5)(c=(6,7))
# /?a=1&a=2&a=3&b=4&b=5&c=6&c=7
```

Convert `URLPath` to string:

```python
url = str(URLPath('/foo/bar/baz'))
```

Concatenate using `+` and `/` (because, hey, why not!):

```python
start = '/start/of/path'
middle = URLPath('middle')
end = '/end/of/path'

# supports both URLPath and string concatenation

URLPath(start) + middle + URLPath(end)
URLPath(start) + middle + end
start + middle + URLPath(end)

URLPath(start) / middle / URLPath(end)
URLPath(start) / middle / end
start / middle / URLPath(end)
```


### OSPath

See all the stuff `URLPath` can do above? If you limit it to the path generation parts, then `OSPath` works the same way but instead of creating fancy URLs, it creates awesome OS paths!

```python
from ladder import OSPath

var = OSPath('/var')
print(var.www.mydir)
# /var/www/mydir (on Unix)
```


### DelimitedPath

Take `OSPath` and tell it to use any string delimiter you'd like and you get something like `DelimitedPath`.

```python
from ladder import DelimitedPath

PeriodPath = DelimitedPath(delimiter='.')

mypath = PeriodPath('foo').bar.baz('qux')
print(mypath)
# foo.bar.baz.qux
```


### API

Do what `URLPath` does but make an HTTP request at the end (_provided you give it a client_)! Now we're really trying to be like `hammock`.

After installing [requests]:

```python
import requests
from ladder import API

# If you need to configure your requests session,
# it's best to do it before passing it into API().
Hammock = API(requests.session())

# However, if you can't preconfigure the requests session...
Hammock.__client__.auth = ('user', 'pass')
Hammock.__client__.headers.update({'x-test': True})

github = Hammock('https://api.github.com')
results = github.search.repositories(q='ladder').GET().json()

api = Hammock('https://api.example.com')
data = {'a': 1, 'b': 2}
api.users.POST(data, headers={}, auth=()).json()
api.users(1).PUT(data).json()
api.users(1).DELETE().json()
api.users.HEAD()
api.users.OPTIONS()
```

Don't like having to use UPPERCASE HTTP METHODS? No problem! `API` has you covered:

```python
github = API(requests.session(), 'https://api.github.com', upper_methods=False)
results = github.search.repositories(q='ladder').get().json()
```

Just remember you'll need to pass a `string` for any of the lowercase HTTP methods that are in the URL path:

```python
api = API(requests.session(), '/api/', upper_methods=False)
api.item('get').details.get()
```

[hammock]: https://github.com/kadirpekel/hammock
[requests]: https://github.com/kennethreitz/requests
[flask]: http://flask.pocoo.org/
