## v0.2.4 (2014-05-06)

- Remove usage of `deepcopy` and ensure `URL` state isn't modified during regeneration.

## v0.2.3 (2014-05-06)

- Fix bug where including params in `URL()` resulted in previous instance's params being modified, i.e., `x = URL('/'); y = x(a=1)` resulted in `a=1` being added to `x`.

## v0.2.2 (2014-04-01)

- Support mulitple query parameters instead of overriding with last supplied.

## v0.2.1 (2014-03-27)

- Remove falsey path values in `ladder.urlpathjoin`.
- Extract query string from url path and merge with existing params.

## v0.2.0 (2014-03-27)

- Rename `ladder.Ladder` to `ladder.API`. **breaking change**
- Rename argument `uppercase_methods` in `API` to `upper_methods`. **breaking change**

## v0.1.0 (2014-03-26)

- First release
