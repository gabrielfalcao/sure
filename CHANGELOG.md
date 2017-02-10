# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

*Nothing to release yet*

## [v1.4.1]
### Added
- Python 3.6 support
- Python 3.7-dev support (allowed to fail)

### Fixed
- Do not overwrite existing class and instance attributes with sure properties (when. should, ...). Refs #127, #129
- Fix patched built-in `dir()` method. Refs #124, #128

## [v1.4.0]
### Added
- anything object which is accessible with `sure.anything`
- interface to extend sure. Refs #31

### Removed
- Last traces of Python 2.6 support

### Fixed
- Allow overwriting of monkey-patched properties by sure. Refs #19
- Assertions for raises

## [v1.3.0]
### Added
- Python 3.3, 3.4 and 3.5 support
- pypy support
- Support comparison of OrderedDict. Refs #55

### Fixed
- `contain` assertion. Refs #104


## No previous changelog history.

Please see `git log`

[Unreleased]: https://github.com/gabrielfalcao/sure/compare/v1.4.1...HEAD
[v1.4.1]: https://github.com/gabrielfalcao/sure/compare/1.4.0...v1.4.1
[v1.4.0]: https://github.com/gabrielfalcao/sure/compare/1.3.0...v1.4.0
[v1.3.0]: https://github.com/gabrielfalcao/sure/compare/1.2.9...v1.3.0
[1.2.9]: https://github.com/gabrielfalcao/sure/compare/1.2.5...1.2.9
[1.2.5]: https://github.com/gabrielfalcao/sure/compare/1.2.4...1.2.5
