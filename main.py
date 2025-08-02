from src.Front.Logging.logging import setup_logger, log_exception
from src.Back.Exceptions.exceptions import BackendDatabaseError, BackendAPIError
from src.Front.Exceptions.exceptions import FrontendValidationError, FrontendRenderingError
from src.Back.Logging.logging import setup_logger as setup_backend_logger, log_exception as log_backend_exception





# Frontend example
frontend_logger = setup_logger("frontend", log_file="frontend.log")
try:
    user_input = "invalid@email"
    if "@" not in user_input:
        raise FrontendValidationError("Invalid email format", input_data=user_input)
except FrontendValidationError as e:
    log_exception(frontend_logger, e, "Frontend validation failed")
    print("Frontend error occurred, check frontend.log")

try:
    component = "MainView"
    raise FrontendRenderingError("Failed to render component", component=component)
except FrontendRenderingError as e:
    log_exception(frontend_logger, e, "Frontend rendering issue")
    print("Frontend error occurred, check frontend.log")

# Backend example
backend_logger = setup_backend_logger("backend", log_file="backend.log")
try:
    query = "SELECT * FROM users WHERE id = 'invalid'"
    raise BackendDatabaseError("Database query failed", query=query)
except BackendDatabaseError as e:
    log_backend_exception(backend_logger, e, "Backend database error")
    print("Backend error occurred, check backend.log")

try:
    raise BackendAPIError("API request failed", status_code=500)
except BackendAPIError as e:
    log_backend_exception(backend_logger, e, "Backend API error")
    print("Backend error occurred, check backend.log")