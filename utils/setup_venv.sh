#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define variables
PYTHON_VERSION="python3.8"  # Replace with your desired Python version
VENV_DIR="venv"            # Name of the virtual environment directory
REQUIREMENTS_FILE="requirements.txt" # Name of the requirements file (if available)

# Step 1: Check if Python is installed
if ! command -v ${PYTHON_VERSION} &> /dev/null; then
    echo "Error: ${PYTHON_VERSION} is not installed."
    echo "Install ${PYTHON_VERSION} and try again."
    exit 1
fi

# Step 2: Create the virtual environment
if [ -d "${VENV_DIR}" ]; then
    echo "Virtual environment '${VENV_DIR}' already exists."
else
    echo "Creating virtual environment '${VENV_DIR}'..."
    ${PYTHON_VERSION} -m venv ${VENV_DIR}
    echo "Virtual environment '${VENV_DIR}' created successfully."
fi

# Step 3: Activate the virtual environment
echo "Activating virtual environment..."
source ${VENV_DIR}/bin/activate

# Step 4: Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Step 5: Install dependencies (if requirements.txt exists)
if [ -f "${REQUIREMENTS_FILE}" ]; then
    echo "Installing dependencies from '${REQUIREMENTS_FILE}'..."
    pip install -r ${REQUIREMENTS_FILE}
else
    echo "No '${REQUIREMENTS_FILE}' found. Skipping dependency installation."
fi

# Step 6: Confirmation
echo "Virtual environment setup complete. To activate it, run:"
echo "source ${VENV_DIR}/bin/activate"
