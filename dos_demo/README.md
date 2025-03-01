# DoS Demonstration Project 🚨

This directory contains a collection of Python scripts that demonstrate various Denial of Service (DoS) attack techniques. These scripts are for **educational purposes only** and should be used **responsibly** in **controlled environments**.

## Scripts 📜

- `single_thread.py`: A single-threaded DoS script that sends continuous HTTP GET requests to a specified target URL.
- `multi_threaded.py`: A multi-threaded DoS script with improved performance and error handling, using connection pooling, thread-local sessions, and retry strategies.

## multi_threaded.py Details 📊

The `multi_threaded.py` script demonstrates an advanced multi-threaded DoS attack with several key features:

- Uses multiple processes, each running multiple threads, to maximize concurrency and resource utilization
- Implements connection pooling with `requests.Session` to reuse connections and reduce overhead 
- Utilizes thread-local storage to provide each thread with its own `Session` instance
- Configures automatic retries with backoff for failed requests
- Tracks and logs request statistics, including status codes, response times, and running averages/maximums
- Handles errors gracefully and backs off on failures to avoid overwhelming the attacker system
- Supports clean termination of all processes and threads via a shared `stop_flag`

These techniques allow for a highly efficient and robust DoS attack, while also providing detailed insights into the attack progress and performance.

## Setup & Usage ⚙️

[Refer to the root `README.md` file](https://github.com/AndrewPBerg/DoS_project/tree/main) for detailed setup instructions, including installing the required dependencies using the uv package manager.

- You can run the following command to set up the environment and install dependencies:
   ```bash
   cd dos_demo
   uv run multi_threaded.py
   ```

## Disclaimer ⚠️

**This project is for educational purposes only. Launching DoS attacks against systems without explicit permission is illegal and unethical.** The scripts provided in this directory are intended to demonstrate the concepts and techniques involved in DoS attacks and should only be used in controlled environments with proper authorization.

**The authors and contributors of this project are not responsible for any misuse or damage caused by the code. Use this code responsibly and only on systems you own or have permission to test. Never target systems without prior consent.**

Unauthorized DoS attacks can lead to criminal charges and severe penalties. It is crucial to understand the legal and ethical implications before running these scripts. Always act responsibly and respect the law.
