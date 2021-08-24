# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.1.1] - 2021-08-24

### Added
- Example of using Python multiprocessing to run both judge and agent within one program.

### Fixed
- Incorrect place of binding listening socket in `JudgeEnv` that prevents multiprocessing
from working properly.

## [0.1.0] - 2021-08-20

### Added
- Initialize project