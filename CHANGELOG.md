# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

# [0.2.0] - 2021-10-15

### Changed
- (Breaking) socket binding for `JudgeEnv` and `JudgeMultiEnv` are separated from `start`
method into `bind` method. (Now before calling `start` you need to call `bind` first.)
- (Breaking) `port` is no longer optional for `AgentEnv`
- (Breaking) `port` now defaults to `None` (i.e. use a random available port) for 
`JudgeEnv` and `JudgeMultiEnv`
- Updated examples to reflect these breaking changes - especially for "multiproc" examples.

### Added
- When initializing `JudgeEnv` or `JudgeMultiEnv`, if `port` is not provided, or `None`,
or 0, a random available port will be used in `bind` method. `bind` method will always
return the port number used by this judge instance.

## [0.1.3] - 2021-08-27

### Fixed
- No longer calls `logging.basicConfig` in `__init__.py` (otherwise importing this module
would invalidate all subsequent logger configs).

## [0.1.2] - 2021-08-27

### Added
- Examples of using multiprocessing to run multi-agent judge env and several agents within
one program.
- Ignoring render/seed/close requests in JudgeMultiEnv (as for how to handle these
methods properly, please refer to how `close` is handled in `./example/multiproc_multi.py`).
- Code formatted by black formatter.

## [0.1.1] - 2021-08-24

### Added
- Example of using Python multiprocessing to run both judge and agent within one program.

### Fixed
- Incorrect place of binding listening socket in `JudgeEnv` that prevents multiprocessing
from working properly.

## [0.1.0] - 2021-08-20

### Added
- Initialize project