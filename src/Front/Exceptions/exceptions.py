class FrontValidationError(Exception):
    """Raised when there is a validation error."""
    pass


class FrontAuthenticationError(Exception):
    """Raised when there is an authentication error."""
    pass


class FrontAuthorizationError(Exception):
    """Raised when there is an authorization error."""
    pass


class FrontDatabaseError(Exception):
    """Raised when there is a database-related error."""
    pass


class FrontNotFoundError(Exception):
    """Raised when a requested resource is not found."""
    pass


class FrontTimeoutError(Exception):
    """Raised when an operation times out."""
    pass


class FrontConnectionError(Exception):
    """Raised when there is a connection error."""
    pass


class FrontConfigurationError(Exception):
    """Raised when there is a configuration issue."""
    pass


class FrontDependencyError(Exception):
    """Raised when a required dependency is missing or fails."""
    pass


class FrontFileProcessingError(Exception):
    """Raised when there is an error processing a file."""
    pass