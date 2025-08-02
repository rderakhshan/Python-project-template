from datetime import datetime

class BackendError(Exception):
    """Base exception for backend-related errors."""
    pass

class BackendDatabaseError(BackendError):
    """Raised when a database operation fails in the backend.
    
    Attributes:
        message (str): Explanation of the error.
        query (str): The database query that failed.
        timestamp (datetime): Time the error occurred.
    """
    def __init__(self, message, query=None):
        self.message = message
        self.query = query
        self.timestamp = datetime.now()
        super().__init__(self.message)
    
    def __str__(self):
        return f"[{self.timestamp}] {self.message} (Query: {self.query if self.query else 'None'})"

class BackendAPIError(BackendError):
    """Raised when an API call fails in the backend.
    
    Attributes:
        message (str): Explanation of the error.
        status_code (int): HTTP status code of the failed API call.
    """
    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.message} (Status Code: {self.status_code if self.status_code else 'None'})"

class BackendAuthenticationError(BackendError):
    """Raised when authentication fails in the backend.
    
    Attributes:
        message (str): Explanation of the error.
        user_id: The user ID associated with the failure.
    """
    def __init__(self, message, user_id=None):
        self.message = message
        self.user_id = user_id
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.message} (User ID: {self.user_id if self.user_id else 'None'})"

class BackendConfigurationError(BackendError):
    """Raised when configuration settings are invalid in the backend.
    
    Attributes:
        message (str): Explanation of the error.
        config_key (str): The invalid configuration key.
    """
    def __init__(self, message, config_key=None):
        self.message = message
        self.config_key = config_key
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.message} (Config Key: {self.config_key if self.config_key else 'None'})"
