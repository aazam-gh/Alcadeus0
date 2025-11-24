#!/usr/bin/env python3
"""
Validation script to verify the backend setup is correct.
This script checks imports, configuration, and file structure.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))


def check_file_exists(filepath: str) -> bool:
    """Check if a file exists."""
    return os.path.isfile(filepath)


def check_directory_exists(dirpath: str) -> bool:
    """Check if a directory exists."""
    return os.path.isdir(dirpath)


def validate_structure() -> bool:
    """Validate the project structure."""
    print("Checking project structure...")
    
    required_files = [
        "pyproject.toml",
        "Dockerfile",
        ".dockerignore",
        "alembic.ini",
        "app/main.py",
        "app/core/config.py",
        "app/database/engine.py",
        "migrations/env.py",
        "migrations/versions/001_initial_schema.py",
    ]
    
    required_dirs = [
        "app",
        "app/api",
        "app/core",
        "app/database",
        "app/models",
        "app/schemas",
        "migrations",
        "migrations/versions",
    ]
    
    all_good = True
    
    for file in required_files:
        if check_file_exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ MISSING: {file}")
            all_good = False
    
    for directory in required_dirs:
        if check_directory_exists(directory):
            print(f"  ✓ {directory}/")
        else:
            print(f"  ✗ MISSING: {directory}/")
            all_good = False
    
    return all_good


def validate_python_syntax() -> bool:
    """Validate Python file syntax."""
    print("\nChecking Python syntax...")
    
    import py_compile
    import pathlib
    
    all_good = True
    python_files = pathlib.Path(".").glob("**/*.py")
    
    for pyfile in python_files:
        try:
            py_compile.compile(str(pyfile), doraise=True)
            print(f"  ✓ {pyfile}")
        except py_compile.PyCompileError as e:
            print(f"  ✗ {pyfile}: {e}")
            all_good = False
    
    return all_good


def validate_imports() -> bool:
    """Validate that critical imports would work (when dependencies are installed)."""
    print("\nChecking import paths...")
    
    import_paths = [
        "app.core.config",
        "app.database.engine",
        "app.models.account",
        "app.models.technician",
        "app.models.job",
        "app.models.invoice",
        "app.schemas.health",
        "app.api.health",
    ]
    
    all_good = True
    
    for import_path in import_paths:
        module_parts = import_path.split(".")
        file_path = os.path.join(*module_parts[:-1], module_parts[-1] + ".py")
        
        if os.path.exists(file_path):
            print(f"  ✓ {import_path} ({file_path})")
        else:
            print(f"  ✗ MISSING: {import_path} ({file_path})")
            all_good = False
    
    return all_good


def main():
    """Run all validations."""
    print("=" * 60)
    print("Backend Setup Validation")
    print("=" * 60)
    
    os.chdir(os.path.dirname(__file__))
    
    results = []
    results.append(("Project Structure", validate_structure()))
    results.append(("Python Syntax", validate_python_syntax()))
    results.append(("Import Paths", validate_imports()))
    
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All validations passed! Backend setup is ready.")
        print("\nNext steps:")
        print("1. Create a .env file with your configuration")
        print("2. Install dependencies: poetry install")
        print("3. Apply migrations: alembic upgrade head")
        print("4. Start the server: uvicorn app.main:app --reload")
        return 0
    else:
        print("\n✗ Some validations failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
