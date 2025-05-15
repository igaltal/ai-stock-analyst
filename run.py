#!/usr/bin/env python3
import os
import subprocess
import time
import sys
import signal
import argparse

def start_api():
    """Start the Flask API server."""
    print("Starting Flask API...")
    python_path = sys.executable
    api_process = subprocess.Popen([python_path, 'app.py'])
    return api_process

def start_ui():
    """Start the Streamlit UI."""
    print("Starting Streamlit UI...")
    venv_dir = os.path.dirname(os.path.dirname(sys.executable))
    streamlit_path = os.path.join(venv_dir, 'bin', 'streamlit')
    ui_process = subprocess.Popen([streamlit_path, 'run', 'streamlit_app.py'])
    return ui_process

def signal_handler(sig, frame):
    """Handle Ctrl+C to gracefully terminate the application."""
    print("\nShutting down services...")
    sys.exit(0)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run AI Stock Analyst components")
    parser.add_argument("--api-only", action="store_true", help="Run only the API server")
    parser.add_argument("--ui-only", action="store_true", help="Run only the Streamlit UI")
    args = parser.parse_args()
    
    # Set up signal handler for graceful termination
    signal.signal(signal.SIGINT, signal_handler)
    
    processes = []
    
    try:
        # Start components based on arguments
        if args.api_only:
            api_process = start_api()
            processes.append(api_process)
        elif args.ui_only:
            ui_process = start_ui()
            processes.append(ui_process)
        else:
            # Start both by default
            api_process = start_api()
            # Wait for API to start
            time.sleep(3)
            ui_process = start_ui()
            processes.extend([api_process, ui_process])
        
        # Wait for all processes to finish (or until interrupted)
        for process in processes:
            process.wait()
    
    except KeyboardInterrupt:
        print("\nShutting down services...")
    finally:
        # Clean up processes
        for process in processes:
            if process.poll() is None:  # If process is still running
                process.terminate()
                process.wait()
        print("All services stopped.")

if __name__ == "__main__":
    main() 