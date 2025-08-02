from datetime import datetime

class FrontendError(Exception):
    """Base exception for frontend-related errors."""
    pass

class FrontendValidationError(FrontendError):
    """Raised when user input validation fails in the frontend.
    
    Attributes:
        message (str): Explanation of the error.
        input_data: The invalid input that caused the error.
        timestamp (datetime): Time the error occurred.
    """
    def __init__(self, message, input_data=None):
        self.message = message
        self.input_data = input_data
        self.timestamp = datetime.now()
        super().__init__(self.message)
    
    def __str__(self):
        return f"[{self.timestamp}] {self.message} (Input: {self.input_data if self.input_data else 'None'})"

class FrontendRenderingError(FrontendError):
    """Raised when rendering fails in the frontend.
    
    Attributes:
        message (str): Explanation of the error.
        component (str): The component that failed to render.
    """
    def __init__(self, message, component=None):
        self.message = message
        self.component = component
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.message} (Component: {self.component if self.component else 'None'})"

class FrontendConnectionError(FrontendError):
    """Raised when a connection to an external service fails in the frontend.
    
    Attributes:
        message (str): Explanation of the error.
        service (str): The external service that failed.
    """
    def __init__(self, message, service=None):
        self.message = message
        self.service = service
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.message} (Service: {self.service if self.service else 'None'})"

class FrontendConfigurationError(FrontendError):
    """Raised when configuration settings are invalid in the frontend.
    
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
