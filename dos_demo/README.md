# DoS Demonstration Project

This project provides a demonstration of a Denial of Service (DoS) attack using Python. It includes three scripts:

1. `single_thread.py`: A single-threaded DoS script
2. `multi_threaded.py`: A multi-threaded DoS script with improved performance and error handling
3. `sockets.py`: A multi-threaded DoS script using raw sockets

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

## Disclaimer

This project is for educational purposes only. Launching DoS attacks against systems without explicit permission is illegal and unethical. The scripts provided in this project, including `sockets.py`, are intended to demonstrate the concepts and techniques involved in DoS attacks and should only be used in controlled environments with proper authorization. The authors and contributors of this project are not responsible for any misuse or damage caused by the code. Use this code responsibly and only on systems you own or have permission to test.
