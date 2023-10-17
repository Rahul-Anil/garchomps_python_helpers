# Python helpers

Template and Helper for quick use

## Log templates

usage example:

### logTemplate package
Example usage:
```python
from logTemplate import make_logger

logger = make_logger.init_logger(logging_config_path, logger_name)
```

## Feature flags
Will contain a feature flag helper for quick use for general use feature flags to
set within the code and not in the environment
TODO: set the feature flags into the environment`

### featureFlags package

#### dev_cycle module
Example usage:
```python
from featureFlags import dev_cycle

dev_cycle_flag = dev_cycle.DevStatus.DEVELOPMENT
```

DevStatus feature flags are:
- *DEVELOPMENT*: during development
- *TESTING*: during testing
- *PRODUCTION*: during production
