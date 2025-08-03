import subprocess
import re
import toml
import os

def add_requirements_to_pyproject(requirements_file="requirements.txt"):
    """
    Clears all dependencies from pyproject.toml, adds packages from a requirements.txt file
    using the `uv add` command, and creates a source package skeleton in the project directory.
    The skeleton includes a 'src' directory with an '__init__.py' file, containing two subdirectories,
    'Front' and 'Back', each with an '__init__.py' file and subdirectories 'components', 'Logging',
    'Exceptions', 'Constants', and 'Utils'. Each subdirectory contains an '__init__.py' file and a
    specific Python file: 'logging.py' with logging utilities, 'exceptions.py' with custom exception
    classes, 'constants.py', or 'utils.py'. The 'components' directory includes 'StageOne.py',
    'StageTwo.py', and 'StageThree.py'. Additionally, a 'configs' directory is created in the project
    root with a 'configuration.yml' file containing industry-standard configuration settings.

    Functionality:
        - Clears the [project.dependencies] section in pyproject.toml.
        - Parses package specifications from requirements.txt, ignoring comments and empty lines.
        - Uses a regular expression to extract package names and version constraints.
        - Executes `uv add` for each valid package to update pyproject.toml and install it.
        - Creates the source package structure under 'src/Front' and 'src/Back' with specified subdirectories and files.
        - Creates the 'configs' directory with a 'configuration.yml' file in the project root.
        - Includes template code for 'logging.py', 'exceptions.py', and 'configuration.yml'.
        - Handles errors such as missing files, invalid package specifications, or failed commands.
        - Provides feedback on the success or failure of each operation.

    Logic:
        1. Load pyproject.toml and clear the [project.dependencies] section.
        2. Read requirements.txt line by line.
        3. Parse each line to extract package names and version constraints.
        4. Skip invalid lines or comments.
        5. Run `uv add` for each valid package to update pyproject.toml and install it.
        6. Save the updated pyproject.toml.
        7. Create the 'configs' directory with 'configuration.yml' and the 'src' directory with
           '__init__.py', and 'Front' and 'Back' subdirectories with their files.
        8. Return True if all operations succeed, False if any step fails.

    Args:
        requirements_file (str): Path to the requirements.txt file. Defaults to "requirements.txt"
                                in the current directory.

    Returns:
        bool: True if dependencies were cleared, all packages were added successfully, and the
              package skeleton and configuration file were created, False if any error occurs
              (e.g., file not found, invalid package, or failed command).

    Raises:
        FileNotFoundError: If requirements.txt or pyproject.toml does not exist.
        subprocess.CalledProcessError: If a `uv add` command fails.
        Exception: For unexpected errors during file reading, writing, or directory creation.

    Example:
        >>> add_requirements_to_pyproject("requirements.txt")
        Clearing existing dependencies in pyproject.toml...
        Successfully cleared dependencies.
        Adding numpy to pyproject.toml...
        Successfully added numpy: ...
        Adding pandas to pyproject.toml...
        Successfully added pandas: ...
        All packages added successfully.
        Creating source package skeleton...
        Successfully created configs with configuration.yml
        Successfully created src with __init__.py
        Successfully created src/Front with __init__.py
        Successfully created src/Front/components with StageOne.py, StageTwo.py, StageThree.py, and __init__.py
        Successfully created src/Front/Logging with __init__.py and logging.py
        Successfully created src/Front/Exceptions with __init__.py and exceptions.py
        Successfully created src/Front/Constants with __init__.py and constants.py
        Successfully created src/Front/Utils with __init__.py and utils.py
        Successfully created src/Back with __init__.py
        Successfully created src/Back/components with StageOne.py, StageTwo.py, StageThree.py, and __init__.py
        Successfully created src/Back/Logging with __init__.py and logging.py
        Successfully created src/Back/Exceptions with __init__.py and exceptions.py
        Successfully created src/Back/Constants with __init__.py and constants.py
        Successfully created src/Back/Utils with __init__.py and utils.py
        True

    Notes:
        - Requires `uv` and `toml` (or `tomli`/`tomli-w`) to be installed and accessible.
        - Supports common requirements.txt formats (e.g., "package==version", "package>=version", "package").
        - Does not support complex formats like URLs, editable installs, or environment markers.
        - After running, use `uv sync` to ensure the environment matches pyproject.toml.
        - If pyproject.toml does not exist, it creates a minimal one with a [project] section.
        - The source package skeleton is created in the current working directory under 'src'.
        - The 'configs' directory is created in the project root with a 'configuration.yml' file.
        - Existing directories or files are not overwritten to avoid data loss.
        - Template code is included in 'logging.py' for logging utilities, 'exceptions.py' for custom
          exceptions, and 'configuration.yml' for project configuration.
    """
    # Block 1: Clear existing dependencies in pyproject.toml
    # Purpose: Loads pyproject.toml and clears the [project.dependencies] section.
    # Input: None (uses default pyproject.toml file).
    # Output: Updates pyproject.toml with an empty dependencies list or creates a new file if missing.
    try:
        try:
            with open("pyproject.toml", 'r') as f:
                pyproject = toml.load(f)  # Load existing pyproject.toml
        except FileNotFoundError:
            pyproject = {'project': {'name': 'my-project', 'version': '0.1.0', 'dependencies': []}}  # Create minimal structure if file is missing

        print("Clearing existing dependencies in pyproject.toml...")
        pyproject.setdefault('project', {}).setdefault('dependencies', [])  # Ensure [project.dependencies] exists
        pyproject['project']['dependencies'] = []  # Clear dependencies
        with open("pyproject.toml", 'w') as f:
            toml.dump(pyproject, f)  # Save updated pyproject.toml
        print("Successfully cleared dependencies.")

    except Exception as e:
        print(f"Error clearing pyproject.toml: {str(e)}")  # Log any errors during file handling
        return False

    # Block 2: Read the requirements.txt file
    # Purpose: Opens and reads the requirements.txt file to extract package specifications.
    # Input: The file path provided in requirements_file.
    # Output: A list of lines from the file, or raises FileNotFoundError if the file is missing.
    try:
        with open(requirements_file, 'r') as f:
            lines = f.readlines()

        # Block 3: Initialize package parsing
        # Purpose: Sets up a regular expression to parse package names and version constraints.
        # Input: None (defines the regex pattern).
        # Output: A compiled regex pattern to match package specifications.
        package_pattern = re.compile(r'^([a-zA-Z0-9][a-zA-Z0-9._-]*)([=><!~]+.*)?$')  # Matches package name and optional version constraint

        # Block 4: Process each line and execute `uv add`
        # Purpose: Iterates through each line, parses valid package specifications, and runs `uv add'.
        # Input: List of lines from requirements.txt.
        # Output: Executes `uv add` for each valid package, prints status, and returns True/False based on success.
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace
            if not line or line.startswith('#'):
                continue  # Skip empty lines and comments

            # Parse the line to extract package name and version constraint
            match = package_pattern.match(line)
            if not match:
                print(f"Skipping invalid line: {line}")  # Log invalid lines for user awareness
                continue

            package_name, version_constraint = match.groups()  # Extract package name and version (if any)
            if version_constraint:
                package_spec = f"{package_name}{version_constraint}"  # Combine for exact specification
            else:
                package_spec = package_name  # Use package name only if no version constraint

            # Execute `uv add` command
            print(f"Adding {package_spec} to pyproject.toml...")
            try:
                result = subprocess.run(
                    ["uv", "add", package_spec],  # Construct `uv add` command
                    check=True,  # Raise an error if the command fails
                    text=True,  # Capture output as text
                    capture_output=True  # Capture stdout and stderr
                )
                print(f"Successfully added {package_spec}: {result.stdout}")  # Log success
            except subprocess.CalledProcessError as e:
                print(f"Failed to add {package_spec}: {e.stderr}")  # Log failure with error details
                return False

        print("All packages added successfully.")  # Indicate completion of all additions

        # Block 5: Create source package skeleton and configuration directory
        # Purpose: Creates the 'configs' directory with a 'configuration.yml' file in the project root.
        #          Creates the 'src' directory with an '__init__.py' file, containing 'Front' and 'Back'
        #          subdirectories. Each of 'Front' and 'Back' has an '__init__.py' file and subdirectories
        #          'components', 'Logging', 'Exceptions', 'Constants', and 'Utils'. Each subdirectory contains
        #          an '__init__.py' file and a specific Python file: 'logging.py' with logging utilities,
        #          'exceptions.py' with custom exception classes, 'constants.py', or 'utils.py'. The 'components'
        #          directory includes 'StageOne.py', 'StageTwo.py', and 'StageThree.py'.
        # Input: None (uses current working directory).
        # Output: Creates the directory structure and files, prints status, and returns True/False.
        try:
            print("Creating source package skeleton...")

            # Create configs directory with configuration.yml
            configs_dir = os.path.join(os.getcwd(), "configs")
            os.makedirs(configs_dir, exist_ok=True)  # Create configs directory if it doesn't exist
            config_file = os.path.join(configs_dir, "configuration.yml")
            if not os.path.exists(config_file):
                config_template = """# Configuration file for the project
# Supports multiple environments (dev, prod) and settings for frontend, backend, database, logging, and API

environments:
  dev:
    debug: true
    logging:
      level: DEBUG
      file: logs/dev.log
    frontend:
      api_endpoint: http://localhost:3000/api
      timeout: 10
      max_retries: 3
    backend:
      database:
        host: localhost
        port: 5432
        name: dev_db
        user: dev_user
        password: dev_password
      api:
        base_url: http://localhost:8000
        key: dev_api_key
        timeout: 30
  prod:
    debug: false
    logging:
      level: INFO
      file: logs/prod.log
    frontend:
      api_endpoint: https://api.production.com
      timeout: 15
      max_retries: 5
    backend:
      database:
        host: prod.db.server.com
        port: 5432
        name: prod_db
        user: prod_user
        password: prod_password
      api:
        base_url: https://api.production.com
        key: prod_api_key
        timeout: 60
"""
                with open(config_file, 'w') as f:
                    f.write(config_template)  # Write configuration.yml
                print("Successfully created configs with configuration.yml")

            # Create src directory
            src_dir = os.path.join(os.getcwd(), "src")  # Path to src directory
            os.makedirs(src_dir, exist_ok=True)  # Create src directory if it doesn't exist
            
            # Create __init__.py in src directory
            src_init_file = os.path.join(src_dir, "__init__.py")
            if not os.path.exists(src_init_file):
                with open(src_init_file, 'w') as f:
                    f.write("")  # Create empty __init__.py in src
            print("Successfully created src with __init__.py")

            # Define main subdirectories (Front and Back)
            main_subdirs = ["Front", "Back"]

            # Define subdirectories and their specific Python files
            subdirs = [
                ("components", ["StageOne.py", "StageTwo.py", "StageThree.py"]),
                ("Logging", ["logging.py"]),
                ("Exceptions", ["exceptions.py"]),
                ("Constants", ["constants.py"]),
                ("Utils", ["utils.py"])
            ]

            # Template for logging.py
            logging_template_front = """import logging

def setup_logger(name, log_file='frontend.log', level=logging.INFO):
    \"\"\"Configure and return a logger for frontend components.
    
    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file. Defaults to 'frontend.log'.
        level: Logging level (e.g., logging.INFO, logging.ERROR).
    
    Returns:
        logging.Logger: Configured logger instance.
    \"\"\"
    logger = logging.getLogger(name)
    if not logger.handlers:  # Avoid duplicate handlers
        logger.setLevel(level)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def log_exception(logger, exception, message):
    \"\"\"Log an exception with additional context.
    
    Args:
        logger (logging.Logger): Logger instance to use.
        exception (Exception): The exception to log.
        message (str): Additional message to include in the log.
    \"\"\"
    logger.error(f\"{message}: {str(exception)}\", exc_info=True)
"""

            logging_template_back = """import logging

def setup_logger(name, log_file='backend.log', level=logging.INFO):
    \"\"\"Configure and return a logger for backend components.
    
    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file. Defaults to 'backend.log'.
        level: Logging level (e.g., logging.INFO, logging.ERROR).
    
    Returns:
        logging.Logger: Configured logger instance.
    \"\"\"
    logger = logging.getLogger(name)
    if not logger.handlers:  # Avoid duplicate handlers
        logger.setLevel(level)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def log_exception(logger, exception, message):
    \"\"\"Log an exception with additional context.
    
    Args:
        logger (logging.Logger): Logger instance to use.
        exception (Exception): The exception to log.
        message (str): Additional message to include in the log.
    \"\"\"
    logger.error(f\"{message}: {str(exception)}\", exc_info=True)
"""

            # Template for exceptions.py
            exceptions_template_front = """from datetime import datetime

class FrontendError(Exception):
    \"\"\"Base exception for frontend-related errors.\"\"\"
    pass

class FrontendValidationError(FrontendError):
    \"\"\"Raised when user input validation fails in the frontend.
    
    Attributes:
        message (str): Explanation of the error.
        input_data: The invalid input that caused the error.
        timestamp (datetime): Time the error occurred.
    \"\"\"
    def __init__(self, message, input_data=None):
        self.message = message
        self.input_data = input_data
        self.timestamp = datetime.now()
        super().__init__(self.message)
    
    def __str__(self):
        return f\"[{self.timestamp}] {self.message} (Input: {self.input_data if self.input_data else 'None'})\"

class FrontendRenderingError(FrontendError):
    \"\"\"Raised when rendering fails in the frontend.
    
    Attributes:
        message (str): Explanation of the error.
        component (str): The component that failed to render.
    \"\"\"
    def __init__(self, message, component=None):
        self.message = message
        self.component = component
        super().__init__(self.message)
    
    def __str__(self):
        return f\"{self.message} (Component: {self.component if self.component else 'None'})\"

class FrontendConnectionError(FrontendError):
    \"\"\"Raised when a connection to an external service fails in the frontend.
    
    Attributes:
        message (str): Explanation of the error.
        service (str): The external service that failed.
    \"\"\"
    def __init__(self, message, service=None):
        self.message = message
        self.service = service
        super().__init__(self.message)
    
    def __str__(self):
        return f\"{self.message} (Service: {self.service if self.service else 'None'})\"

class FrontendConfigurationError(FrontendError):
    \"\"\"Raised when configuration settings are invalid in the frontend.
    
    Attributes:
        message (str): Explanation of the error.
        config_key (str): The invalid configuration key.
    \"\"\"
    def __init__(self, message, config_key=None):
        self.message = message
        self.config_key = config_key
        super().__init__(self.message)
    
    def __str__(self):
        return f\"{self.message} (Config Key: {self.config_key if self.config_key else 'None'})\"
"""

            exceptions_template_back = """from datetime import datetime

class BackendError(Exception):
    \"\"\"Base exception for backend-related errors.\"\"\"
    pass

class BackendDatabaseError(BackendError):
    \"\"\"Raised when a database operation fails in the backend.
    
    Attributes:
        message (str): Explanation of the error.
        query (str): The database query that failed.
        timestamp (datetime): Time the error occurred.
    \"\"\"
    def __init__(self, message, query=None):
        self.message = message
        self.query = query
        self.timestamp = datetime.now()
        super().__init__(self.message)
    
    def __str__(self):
        return f\"[{self.timestamp}] {self.message} (Query: {self.query if self.query else 'None'})\"

class BackendAPIError(BackendError):
    \"\"\"Raised when an API call fails in the backend.
    
    Attributes:
        message (str): Explanation of the error.
        status_code (int): HTTP status code of the failed API call.
    \"\"\"
    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
    
    def __str__(self):
        return f\"{self.message} (Status Code: {self.status_code if self.status_code else 'None'})\"

class BackendAuthenticationError(BackendError):
    \"\"\"Raised when authentication fails in the backend.
    
    Attributes:
        message (str): Explanation of the error.
        user_id: The user ID associated with the failure.
    \"\"\"
    def __init__(self, message, user_id=None):
        self.message = message
        self.user_id = user_id
        super().__init__(self.message)
    
    def __str__(self):
        return f\"{self.message} (User ID: {self.user_id if self.user_id else 'None'})\"

class BackendConfigurationError(BackendError):
    \"\"\"Raised when configuration settings are invalid in the backend.
    
    Attributes:
        message (str): Explanation of the error.
        config_key (str): The invalid configuration key.
    \"\"\"
    def __init__(self, message, config_key=None):
        self.message = message
        self.config_key = config_key
        super().__init__(self.message)
    
    def __str__(self):
        return f\"{self.message} (Config Key: {self.config_key if self.config_key else 'None'})\"
"""

            # Create Front and Back directories with their subdirectories and files
            for main_subdir in main_subdirs:
                main_subdir_path = os.path.join(src_dir, main_subdir)
                os.makedirs(main_subdir_path, exist_ok=True)  # Create Front or Back directory
                main_init_file = os.path.join(main_subdir_path, "__init__.py")
                if not os.path.exists(main_init_file):
                    with open(main_init_file, 'w') as f:
                        f.write("")  # Create empty __init__.py in Front or Back
                print(f"Successfully created src/{main_subdir} with __init__.py")

                # Create subdirectories and files within Front or Back
                for subdir, extra_files in subdirs:
                    subdir_path = os.path.join(main_subdir_path, subdir)
                    os.makedirs(subdir_path, exist_ok=True)  # Create subdirectory if it doesn't exist
                    init_file = os.path.join(subdir_path, "__init__.py")
                    if not os.path.exists(init_file):
                        with open(init_file, 'w') as f:
                            f.write("")  # Create empty __init__.py
                    # Create extra Python files for the subdirectory
                    for extra_file in extra_files:
                        file_path = os.path.join(subdir_path, extra_file)
                        if not os.path.exists(file_path):
                            with open(file_path, 'w') as f:
                                # Write template code for logging.py and exceptions.py
                                if extra_file == "logging.py":
                                    f.write(logging_template_front if main_subdir == "Front" else logging_template_back)
                                elif extra_file == "exceptions.py":
                                    f.write(exceptions_template_front if main_subdir == "Front" else exceptions_template_back)
                                else:
                                    f.write("")  # Create empty Python file for others
                    print(f"Successfully created src/{main_subdir}/{subdir} with __init__.py and {', '.join(extra_files)}")

            return True

        except Exception as e:
            print(f"Error creating source package skeleton: {str(e)}")  # Log errors during directory/file creation
            return False

    # Block 6: Handle exceptions
    # Purpose: Catches and reports errors such as missing files or unexpected issues.
    # Input: Any exceptions raised during file reading or processing.
    # Output: Error message and False return value.
    except FileNotFoundError:
        print(f"Error: {requirements_file} not found.")  # Specific error for missing file
        return False
    except Exception as e:
        print(f"Error: {str(e)}")  # General error for unexpected issues
        return False

if __name__ == "__main__":
    add_requirements_to_pyproject()