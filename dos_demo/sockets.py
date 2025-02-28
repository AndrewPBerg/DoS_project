import socket
import threading

TARGET_IP = "127.0.0.1"
TARGET_PORT = 5000  # Change this to your app's port

def attack():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_IP, TARGET_PORT))
            s.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            s.close()
        except Exception as e:
            print(f"Connection failed: {e}")

# Launch multiple threads
NUM_THREADS = 50
threads = []

for _ in range(NUM_THREADS):
    thread = threading.Thread(target=attack)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
