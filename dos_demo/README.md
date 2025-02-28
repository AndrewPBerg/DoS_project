# DoS Demonstration Project

This project provides a demonstration of a Denial of Service (DoS) attack using Python. It includes three scripts:

1. `single_thread.py`: A single-threaded DoS script
2. `multi_threaded.py`: A multi-threaded DoS script with improved performance and error handling
3. `sockets.py`: A multi-threaded DoS script using raw sockets
4. `advanced_dos.py`: An advanced multi-threaded DoS script with multiple attack methods for educational purposes

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```
     source venv/bin/activate
     ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Single-Threaded Script

The `single_thread.py` script demonstrates a basic DoS attack using a single thread. It sends continuous HTTP GET requests to a specified target URL and logs the response time and status code at regular intervals.

To run the single-threaded script:
```
python single_thread.py
```

Press `Ctrl+C` to stop the script. It will display a summary of the attack, including the total number of requests sent, the average response time, and the maximum response time.

## Multi-Threaded Script

The `multi_threaded.py` script is an enhanced version of the DoS demonstration that uses multiple threads to send requests concurrently. It includes several improvements:

- Connection pooling to reuse connections and reduce socket usage
- Thread-local sessions to prevent conflicts between threads
- Retry strategy with backoff to handle temporary failures
- Small delays between requests to prevent overwhelming the system

To run the multi-threaded script:
```
python multi_threaded.py
```

Press `Ctrl+C` to stop the script. It will display a summary of the attack, similar to the single-threaded version.

### Handling Socket Exhaustion on Windows

When running the multi-threaded script on Windows, you may encounter a `WinError 10048` socket exhaustion error. This occurs because Windows has a limited number of ephemeral ports available for outgoing connections, and the script can quickly exhaust these ports when making rapid requests.

The multi-threaded script addresses this issue by:

1. Using connection pooling to reuse connections and reduce the number of sockets needed
2. Adding small delays between requests to prevent overwhelming the system
3. Implementing a retry strategy with backoff to handle temporary failures more gracefully

These enhancements allow the multi-threaded script to run for longer periods without encountering the socket exhaustion error.

## Sockets Script

The `sockets.py` script is a multi-threaded DoS demonstration that uses raw sockets instead of HTTP requests. It establishes multiple connections to a specified target IP and port, simulating a DoS attack.

### Running the Sockets Script

1. Ensure you have a server running on the specified `TARGET_IP` and `TARGET_PORT` to test against.
2. Open the `sockets.py` file and update the `TARGET_IP` and `TARGET_PORT` variables to match your target server.
3. Run the script:
   ```
   python sockets.py
   ```
4. Press `Ctrl+C` to stop the attack. A summary will be displayed, including the total number of requests sent, the average response time, and the maximum response time.

### Key Features of the Sockets Script

- **Logging**: Uses colored logging to provide real-time feedback on the attack's progress.
- **Threading**: Launches multiple threads to simulate concurrent connections.
- **Statistics Tracking**: Tracks the number of requests and their response times, logging averages and maximums at intervals.
- **Error Handling**: Catches and logs connection errors, with a backoff strategy to avoid overwhelming the target.
- **Graceful Shutdown**: Allows for a clean exit and summary display when interrupted with Ctrl+C.

### Considerations and Limitations

- The `sockets.py` script requires a server to be running on the specified target IP and port. If no server is available, the script will continuously log connection errors.
- The script uses raw sockets, which may be blocked by firewalls or security software. Ensure that the necessary permissions are granted for the script to establish connections.
- The effectiveness of the DoS attack simulated by the `sockets.py` script depends on various factors, such as the target server's configuration, network capacity, and defense mechanisms in place.

## Advanced DoS Script

The `advanced_dos.py` script is an advanced multi-threaded DoS demonstration that implements multiple attack methods for educational purposes. It includes the following attack methods:

1. **Slowloris**: Keeps connections open by sending partial HTTP headers at regular intervals, consuming server resources.
2. **HTTP Flood**: Sends a large number of HTTP requests with random parameters to bypass caching and overwhelm the server.
3. **TCP Connection Flood**: Creates and closes connections rapidly, consuming server resources.
4. **Resource Exhaustion**: Sends large requests with high memory/CPU processing requirements to exhaust server resources.

### Running the Advanced DoS Script

To run the `advanced_dos.py` script, use the following command:

```
python advanced_dos.py [--ip IP] [--port PORT] [--duration DURATION] [--connections CONNECTIONS] [--timeout TIMEOUT] [--attack]
```

- `--ip IP`: Target IP address (default: 127.0.0.1)
- `--port PORT`: Target port (default: 8000)
- `--duration DURATION`: Attack duration in seconds (default: 600)
- `--connections CONNECTIONS`: Maximum connections (default: 500)
- `--timeout TIMEOUT`: Socket timeout in seconds (default: 10)
- `--attack`: Specify the attack method to run. Available options:
  - `--all`: Run all attack methods (default)
  - `--slowloris`: Run only Slowloris attack
  - `--http-flood`: Run only HTTP flood attack
  - `--tcp-flood`: Run only TCP connection flood attack
  - `--resource`: Run only resource exhaustion attack

For example, to run the HTTP flood attack against a target IP of 192.168.0.1 on port 80 for 300 seconds with 1000 maximum connections and a socket timeout of 5 seconds:

```
python advanced_dos.py --ip 192.168.0.1 --port 80 --duration 300 --connections 1000 --timeout 5 --http-flood
```

Press `Ctrl+C` to stop the attack. A summary will be displayed, including the total number of HTTP requests sent, TCP connections established, average response time, and maximum response time.

### Educational Purpose and Responsible Usage

The `advanced_dos.py` script is designed for educational purposes to demonstrate various DoS attack techniques. It should only be used in controlled environments with proper authorization and never against production systems or without explicit permission.

Launching DoS attacks against systems without consent is illegal and unethical. The authors and contributors of this project are not responsible for any misuse or damage caused by this code. Use this script responsibly and only for learning purposes.

## Disclaimer

This project is for educational purposes only. Launching DoS attacks against systems without explicit permission is illegal and unethical. The scripts provided in this project, including `sockets.py`, are intended to demonstrate the concepts and techniques involved in DoS attacks and should only be used in controlled environments with proper authorization. The authors and contributors of this project are not responsible for any misuse or damage caused by the code. Use this code responsibly and only on systems you own or have permission to test.
