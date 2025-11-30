import psutil
import time
import sys
from datetime import datetime

class CPUMonitor:
    """
    A class to monitor CPU usage and alert when threshold is exceeded.
    """
    
    def __init__(self, threshold=80, interval=2):
        """
        Initialize the CPU monitor.
        
        Args:
            threshold (int): CPU usage percentage threshold for alerts (default: 80%)
            interval (int): Time interval in seconds between checks (default: 2 seconds)
        """
        self.threshold = threshold
        self.interval = interval
        self.alert_count = 0
        
    def get_cpu_usage(self):
        """
        Get current CPU usage percentage.
        
        Returns:
            float: Current CPU usage as a percentage
        """
        try:
            # Get CPU usage over a short interval for more accurate reading
            cpu_usage = psutil.cpu_percent(interval=1)
            return cpu_usage
        except Exception as e:
            raise Exception(f"Error retrieving CPU usage: {str(e)}")
    
    def display_alert(self, cpu_usage):
        """
        Display alert message when CPU usage exceeds threshold.
        
        Args:
            cpu_usage (float): Current CPU usage percentage
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.alert_count += 1
        print(f"[{timestamp}] Alert! CPU usage exceeds threshold: {cpu_usage:.1f}%")
    
    def display_status(self, cpu_usage):
        """
        Display normal status message.
        
        Args:
            cpu_usage (float): Current CPU usage percentage
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] CPU usage: {cpu_usage:.1f}%")
    
    def monitor(self):
        """
        Main monitoring loop that continuously checks CPU usage.
        """
        print(f"Starting CPU Monitor...")
        print(f"Threshold: {self.threshold}%")
        print(f"Check interval: {self.interval} seconds")
        print(f"Press Ctrl+C to stop monitoring\n")
        print("Monitoring CPU usage...")
        
        try:
            while True:
                try:
                    # Get current CPU usage
                    cpu_usage = self.get_cpu_usage()
                    
                    # Check if threshold is exceeded
                    if cpu_usage > self.threshold:
                        self.display_alert(cpu_usage)
                    else:
                        # Optionally display normal status (comment out if too verbose)
                        # self.display_status(cpu_usage)
                        pass
                    
                    # Wait before next check
                    time.sleep(self.interval)
                    
                except KeyboardInterrupt:
                    # Re-raise to handle in outer try-except
                    raise
                except Exception as e:
                    print(f"Error during monitoring: {str(e)}")
                    print("Continuing monitoring...")
                    time.sleep(self.interval)
                    
        except KeyboardInterrupt:
            print(f"\n\nMonitoring stopped by user.")
            print(f"Total alerts triggered: {self.alert_count}")
            sys.exit(0)
        except Exception as e:
            print(f"\nFatal error: {str(e)}")
            sys.exit(1)


def main():
    """
    Main function to run the CPU monitor.
    """
    # Configuration
    CPU_THRESHOLD = 80  # Alert threshold in percentage
    CHECK_INTERVAL = 2  # Check interval in seconds
    
    try:
        # Create and start monitor
        monitor = CPUMonitor(threshold=CPU_THRESHOLD, interval=CHECK_INTERVAL)
        monitor.monitor()
        
    except Exception as e:
        print(f"Failed to start CPU monitor: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
    