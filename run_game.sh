#!/bin/bash

# Gomoku Master - Standalone Setup Script
# Works on Windows (Git Bash), Linux, and macOS

# Print colored text
print_color() {
  if [ -t 1 ]; then
    echo -e "\033[1;34m$1\033[0m"
  else
    echo "$1"
  fi
}

# Detect OS
detect_os() {
  case "$(uname -s)" in
    Linux*)     OS="Linux";;
    Darwin*)    OS="Mac";;
    CYGWIN*)    OS="Windows";;
    MINGW*)     OS="Windows";;
    MSYS*)      OS="Windows";;
    *)          OS="Unknown";;
  esac
  print_color "Detected operating system: $OS"
}

# Check Python installation
check_python() {
  if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
  elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
  else
    print_color "Error: Python is not installed. Please install Python 3.6 or higher."
    exit 1
  fi
  
  # Check Python version
  PY_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
  print_color "Python version: $PY_VERSION"
  
  # Check if version is at least 3.6
  major=$(echo "$PY_VERSION" | cut -d'.' -f1)
  minor=$(echo "$PY_VERSION" | cut -d'.' -f2)
  if (( major < 3 || (major == 3 && minor < 6) )); then
    print_color "Error: Python 3.6 or higher is required. You have $PY_VERSION."
    exit 1
  fi
}

# Install dependencies
install_dependencies() {
  print_color "Installing required Python packages..."
  $PYTHON_CMD -m pip install -r requirements.txt
  
  if [ $? -ne 0 ]; then
    print_color "Error: Failed to install required packages. Please check your internet connection and try again."
    exit 1
  fi
  
  print_color "Dependencies installed successfully."
}

# Start the game
start_game() {
  print_color "Starting Gomoku Master..."
  
  # Start the backend server
  $PYTHON_CMD app.py &
  BACKEND_PID=$!
  
  # Wait for the backend to start
  sleep 2
  
  # Open the game in the browser
  if [ "$OS" = "Mac" ]; then
    open http://localhost:5001
  elif [ "$OS" = "Linux" ]; then
    if command -v xdg-open &> /dev/null; then
      xdg-open http://localhost:5001
    elif command -v gnome-open &> /dev/null; then
      gnome-open http://localhost:5001
    else
      print_color "Please open http://localhost:5000 in your browser"
    fi
  elif [ "$OS" = "Windows" ]; then
    start http://localhost:5001
  else
    print_color "Please open http://localhost:5000 in your browser"
  fi
  
  print_color "Gomoku Master is running!"
  print_color "Press Ctrl+C to stop the game"
  
  # Wait for Ctrl+C
  trap "kill $BACKEND_PID; exit" INT TERM
  wait
}

# Main function
main() {
  print_color "Welcome to Gomoku Master!"
  print_color "Setting up the game..."
  
  # Detect OS
  detect_os
  
  # Check Python installation
  check_python
  
  # Install dependencies
  install_dependencies
  
  # Start the game
  start_game
}

# Run the main function
main
