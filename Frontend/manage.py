#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import psutil  # Import the psutil library
import time

def monitor_memory_limit(memory_limit):
    """Monitor memory usage and terminate if it exceeds the limit."""
    process = psutil.Process(os.getpid())
    while True:
        # Check the current memory usage
        memory_usage = process.memory_info().rss  # Resident Set Size
        if memory_usage > memory_limit:
            print(f"Memory limit exceeded: {memory_usage / (1024 * 1024):.2f} MB > {memory_limit / (1024 * 1024):.2f} MB")
            process.terminate()  # Terminate the process
            break
        time.sleep(1)  # Check every second

def limit_cpu_usage(cpu_cores):
    """Limit the CPU usage by setting CPU affinity."""
    process = psutil.Process(os.getpid())
    process.cpu_affinity(cpu_cores)  # Set the CPU affinity to the specified cores

def main():
    """Run administrative tasks."""
    memory_limit = 256 * 1024 * 1024  # 256 MB in bytes
    cpu_cores = [0]  # Limit to the first CPU core (you can change this as needed)

    # Start monitoring memory usage in a separate thread
    import threading
    monitor_thread = threading.Thread(target=monitor_memory_limit, args=(memory_limit,))
    monitor_thread.daemon = True  # Daemonize thread
    monitor_thread.start()

    # Limit CPU usage
    limit_cpu_usage(cpu_cores)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_230.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
