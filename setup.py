import subprocess
import re
import toml
import os

def add_requirements_to_pyproject(requirements_file="requirements.txt"):
    """
    Clears all dependencies from pyproject.toml, adds packages from a requirements.txt file
    using the `uv add` command, and creates a source package skeleton in the project directory.
    The skeleton includes a 'src' directory with an '__init__.py' file, containing two subdirectories,
    'Front' and 'Back'. Each of 'Front' and 'Back' contains an '__init__.py' file and subdirectories
    'components', 'Logging', 'Exceptions', 'Constants', and 'Utils'. Each subdirectory contains 
    an '__init__.py' file and a specific Python file: 'logging.py', 'exceptions.py', 'constants.py', 
    or 'utils.py'. The 'components' directory includes 'StageOne.py', 'StageTwo.py', and 'StageThree.py'.

    Functionality:
        - Clears the [project.dependencies] section in pyproject.toml.
        - Parses package specifications from requirements.txt, ignoring comments and empty lines.
        - Uses a regular expression to extract package names and version constraints.
        - Executes `uv add` for each valid package to update pyproject.toml and install it.
        - Creates the source package structure under 'src/Front' and 'src/Back' with specified subdirectories and files.
        - Handles errors such as missing files, invalid package specifications, or failed commands.
        - Provides feedback on the success or failure of each operation.

    Logic:
        1. Load pyproject.toml and clear the [project.dependencies] section.
        2. Read requirements.txt line by line.
        3. Parse each line to extract package names and version constraints.
        4. Skip invalid lines or comments.
        5. Run `uv add` for each valid package to update pyproject.toml and install it.
        6. Save the updated pyproject.toml.
        7. Create the 'src' directory with '__init__.py', and 'Front' and 'Back' subdirectories with their files.
        8. Return True if all operations succeed, False if any step fails.

    Args:
        requirements_file (str): Path to the requirements.txt file. Defaults to "requirements.txt"
                                in the current directory.

    Returns:
        bool: True if dependencies were cleared, all packages were added successfully, and the 
              source package skeleton was created, False if any error occurs (e.g., file not found, 
              invalid package, or failed command).

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
        - Existing directories or files are not overwritten to avoid data loss.
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
        # Purpose: Iterates through each line, parses valid package specifications, and runs `uv add`.
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

        # Block 5: Create source package skeleton
        # Purpose: Creates the 'src' directory with an '__init__.py' file, containing 'Front' and 'Back' 
        #          subdirectories. Each of 'Front' and 'Back' has an '__init__.py' file and subdirectories 
        #          'components', 'Logging', 'Exceptions', 'Constants', and 'Utils'. Each subdirectory contains 
        #          an '__init__.py' file and a specific Python file: 'logging.py', 'exceptions.py', 
        #          'constants.py', or 'utils.py'. The 'components' directory includes 'StageOne.py', 
        #          'StageTwo.py', and 'StageThree.py'.
        # Input: None (uses current working directory).
        # Output: Creates the directory structure and files, prints status, and returns True/False.
        try:
            print("Creating source package skeleton...")
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
                                f.write("")  # Create empty Python file
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