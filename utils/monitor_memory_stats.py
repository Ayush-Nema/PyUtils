# Monitor the Disk, Memory, and CPU Status of Your Server or execution machine
# pip install psutil


import psutil
import time


def get_disk_usage():
    disk_usage = psutil.disk_usage('/')
    return {
        'total': disk_usage.total,
        'used': disk_usage.used,
        'free': disk_usage.free,
        'percent': disk_usage.percent
    }


def get_memory_usage():
    memory_info = psutil.virtual_memory()
    return {
        'total': memory_info.total,
        'available': memory_info.available,
        'used': memory_info.used,
        'percent': memory_info.percent
    }


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def display_usage():
    disk_usage = get_disk_usage()
    memory_usage = get_memory_usage()
    cpu_usage = get_cpu_usage()

    print(f"Disk Usage: {disk_usage['percent']}%")
    print(f"    Total: {disk_usage['total'] / (1024 ** 3):.2f} GB")
    print(f"    Used: {disk_usage['used'] / (1024 ** 3):.2f} GB")
    print(f"    Free: {disk_usage['free'] / (1024 ** 3):.2f} GB\n")

    print(f"Memory Usage: {memory_usage['percent']}%")
    print(f"    Total: {memory_usage['total'] / (1024 ** 3):.2f} GB")
    print(f"    Used: {memory_usage['used'] / (1024 ** 3):.2f} GB")
    print(f"    Available: {memory_usage['available'] / (1024 ** 3):.2f} GB\n")

    print(f"CPU Usage: {cpu_usage}%\n")


def monitor(interval=5):
    try:
        while True:
            display_usage()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Monitoring stopped.")


if __name__ == "__main__":
    monitor()


"""
Sample output
--------------

Disk Usage: 10.5%
    Total: 460.43 GB
    Used: 12.55 GB
    Free: 106.75 GB

Memory Usage: 81.8%
    Total: 8.00 GB
    Used: 3.27 GB
    Available: 1.45 GB

CPU Usage: 12.9%
"""
