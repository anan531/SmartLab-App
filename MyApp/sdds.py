import psutil
import time


def monitor_cpu_utilization(interval=1, duration=10):
    """
    Monitors CPU utilization.

    Args:
        interval (int): The interval in seconds between checks.
        duration (int): The total duration to monitor in seconds.
    """;
    print("Monitoring CPU Utilization:")
    print(f"{'Time':<10} {'CPU Usage (%)':<15}")
    print("-" * 25)

    end_time = time.time() + duration
    while time.time() < end_time:
        cpu_usage = psutil.cpu_percent(interval=interval)
        print(f"{time.strftime('%H:%M:%S', time.localtime()):<10} {cpu_usage:<15}")

    print("Monitoring Complete.")


if __name__ == "__main__":
    # Example: Monitor for 10 seconds with 1-second intervals
    monitor_cpu_utilization(interval=1, duration=10)
