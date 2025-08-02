def main():
    print("Hello from test!")
    
    # List of packages to check
    packages = [
        "numpy",
        "pandas",
        "openpyxl",
        "sklearn",  # scikit-learn is imported as sklearn
        "scipy",
        "openai",
        "plotly",
    ]
    
    # Check each package
    for package in packages:
        try:
            __import__(package)  # Dynamically import the package
            print(f"Package '{package}' is installed and can be imported.")
        except ImportError:
            print(f"Package '{package}' is NOT installed or cannot be imported.")

if __name__ == "__main__":
    main()