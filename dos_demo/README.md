# DoS Demonstration Project

This directory contains a collection of Python scripts that demonstrate various Denial of Service (DoS) attack techniques. These scripts are for educational purposes only and should be used responsibly in controlled environments.

## Scripts

- `single_thread.py`: A single-threaded DoS script that sends continuous HTTP GET requests to a specified target URL.
- `multi_threaded.py`: A multi-threaded DoS script with improved performance and error handling, using connection pooling, thread-local sessions, and retry strategies.
- `sockets.py`: A multi-threaded DoS script that uses raw sockets to establish multiple connections to a specified target IP and port.
- `advanced_dos.py`: An advanced multi-threaded DoS script with multiple attack methods, including Slowloris, HTTP Flood, TCP Connection Flood, and Resource Exhaustion.

## Setup

Refer to the root `README.md` file for detailed setup instructions, including creating a virtual environment and installing the required dependencies.

## Usage

Each script has its own usage instructions and command-line arguments. Run the scripts with the `-h` or `--help` flag to see the available options.

For example:
```bash
python single_thread.py -h
python multi_threaded.py -h
python sockets.py -h
python advanced_dos.py -h
```

## Disclaimer

This project is for educational purposes only. Launching DoS attacks against systems without explicit permission is illegal and unethical. The scripts provided in this directory are intended to demonstrate the concepts and techniques involved in DoS attacks and should only be used in controlled environments with proper authorization. 

The authors and contributors of this project are not responsible for any misuse or damage caused by the code. Use this code responsibly and only on systems you own or have permission to test.
