# Changelog

## 1.4.0

### Features and enhancements

- Proper handling of exceptions was added to timed decorator.

### Breaking API changes

- Removed striping of whitespaces in unit name. So now ' h ' is not a valid unit name anymore.

### Tests and deployment

- ParamSpec was used to annotate types more precisely in typed decorator.
- Added 1 new test for time formatter.
- Added 4 new tests for Timed context.
- Added 4 new test for timed decorator.
- Restored 3 tests with actual delays with sleep.

### Fun

- New image
- New MIT license badge

### Supported Python versions

- Removed support for 3.8 and 3.9.
- Added support for 3.12.

Supported python versions are 3.10-3.12.

## 1.3.0

### Breaking API changes

- Removed alternative names for time units.

### Features and enhancements

- Type hints were added to the whole codebase.

### Fixes

- Using `interval` property of Timing context before entering the context gives now a RuntimeError with an explanation.
- Using `total` property of Timed iterable returns now zero as expected in case that the iteration was not yet started.

### Docs

- Added this CHANGELOG.

### Tests and deployment

- CI was migrated from CircleCI to GitHub Actions.
- Automatic tests were added for macOS and windows (which were tested before only manually).
- All tests were deeply refactored in this release. All sleeps were replaced with proper mocking of `perf_counter`.
- Unittest and nose was replaced with pytest.
- Static type checker (mypy) was added to CI.

### Supported Python versions

- Removed support for 3.6 and 3.7.
- Added support for 3.10 and 3.11.

Supported python versions are 3.8-3.11.

## 1.2.0

### Features and enhancements

- Use always 3 significant digits when formatting output strings. Such formatting is much more elegant and avoids adding
  decimal points for integers.

### Fixes

- Wrong link in pepy badge.

### Docs

- All docs were rewritten in beautiful numpy style.

### Tests and deployment

- Add CI for python 3.9.
- Use poetry to build and deploy

### Python versions

Supported python versions are 3.6-3.9.

## 1.1.0

### Features and enhancements

- Time units allow aliases, by @johnashu

### Fixes

- Not rescaling total time in Timed iterable - fixed

### Docs

- Add contribution guide.
- Add bug report template.
- Add feature request template.
- Add doc strings in tformatter module.
- Add badges to readme.

### Tests and deployment

- Add CI for python 3.6-3.8
- Add tests of Timed iterable summary
- Add tests of tformatter exception

### Contributors

Thanks to our 1 contributor whose commits are featured in this release:
@johnashu

## 1.0.0

- `horology` name was picked instead of confusing `ttt`.
- The package can now be installed with `pip install horology`.
