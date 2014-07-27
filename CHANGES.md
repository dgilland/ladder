## v0.4.1 (2014-07-26)

- Fix `utils.iterflatten()` by calling `iterflatten()` instead of `flatten` in recursive loop.

## v0.4.0 (2014-06-03)

- Rename `URL` class to `URLPath` for consistency with newly expanded library API. **breaking change**
- Add `DelimitedPath` class to handle path generation using a delimiter.
- Add `OSPath` class to handle OS path generation.
- Add `Ladder` base class for all path generation classes. Cannot be used directly; has to be used as a parent class.

## v0.3.0 (2014-05-19)

- If `URL` param value is a `list` or `tuple`, then flatten it so that each value is mapped to the param key as a separate query parameter (i.e. `a=[1, 2, 3] => '?a=1&a=2&a=3'`).

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
