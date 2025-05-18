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

  # Start the backend server and capture the port from its output
  PORT_LINE=""
  PORT=""
  # Start the server in the background and capture its output
  { $PYTHON_CMD app.py 2>&1 | tee server_output.log & } &
  BACKEND_PID=$!

  # Wait for the backend to start and print the port
  for i in {1..10}; do
    sleep 1
    if [ -f server_output.log ]; then
      PORT_LINE=$(grep -m 1 "Starting Gomoku Master server on port" server_output.log)
      if [ ! -z "$PORT_LINE" ]; then
        PORT=$(echo "$PORT_LINE" | grep -oE '[0-9]+$')
        break
      fi
    fi
  done

  # Fallback if port not found
  if [ -z "$PORT" ]; then
    PORT=5002
    print_color "Warning: Could not detect port from server output. Defaulting to $PORT."
  fi

  # Open the game in the browser
  URL="http://localhost:$PORT"
  if [ "$OS" = "Mac" ]; then
    open "$URL"
  elif [ "$OS" = "Linux" ]; then
    if command -v xdg-open &> /dev/null; then
      xdg-open "$URL"
    elif command -v gnome-open &> /dev/null; then
      gnome-open "$URL"
    else
      print_color "Please open $URL in your browser"
    fi
  elif [ "$OS" = "Windows" ]; then
    start "$URL"
  else
    print_color "Please open $URL in your browser"
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
