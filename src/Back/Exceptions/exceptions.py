class BackValidationError(Exception):
    """Raised when there is a validation error."""
    pass


class BackAuthenticationError(Exception):
    """Raised when there is an authentication error."""
    pass


class BackAuthorizationError(Exception):
    """Raised when there is an authorization error."""
    pass


class BackDatabaseError(Exception):
    """Raised when there is a database-related error."""
    pass


class BackNotFoundError(Exception):
    """Raised when a requested resource is not found."""
    pass


class BackTimeoutError(Exception):
    """Raised when an operation times out."""
    pass


class BackConnectionError(Exception):
    """Raised when there is a connection error."""
    pass


class BackConfigurationError(Exception):
    """Raised when there is a configuration issue."""
    pass


class BackDependencyError(Exception):
    """Raised when a required dependency is missing or fails."""
    pass


class BackFileProcessingError(Exception):
    """Raised when there is an error processing a file."""
    pass