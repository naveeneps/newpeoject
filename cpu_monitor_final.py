"""
CPU Health Monitoring Script

This program continuously monitors CPU usage and alerts when it exceeds a threshold.

Requirements:
    pip install psutil

Usage:
    python cpu_monitor.py

Features:
    - Monitors CPU usage every 2 seconds
    - Displays current CPU utilization
    - Alerts when CPU exceeds 80% threshold
    - Runs indefinitely until Ctrl+C
    - Comprehensive error handling
"""

import psutil
import time
import sys
from datetime import datetime


# Configuration
CPU_THRESHOLD = 80  # Alert threshold in percentage
CHECK_INTERVAL = 2  # Check every 2 seconds


def get_cpu_usage():
    """
    Get current CPU usage percentage.
    
    Returns:
        float: CPU usage percentage
        
    Raises:
        Exception: If unable to retrieve CPU usage
    """
    try:
        # Get CPU usage over 1 second interval for accurate reading
        cpu_percent = psutil.cpu_percent(interval=1)
        return cpu_percent
    except Exception as e:
        raise Exception(f"Error retrieving CPU usage: {str(e)}")


def display_cpu_status(cpu_usage, threshold):
    """
    Display CPU status and alert if threshold exceeded.
    
    Args:
        cpu_usage (float): Current CPU usage percentage
        threshold (float): Alert threshold percentage
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Display current CPU usage
    print(f"[{timestamp}] Current CPU usage: {cpu_usage:.1f}%")
    
    # Check if threshold exceeded
    if cpu_usage > threshold:
        print(f"⚠️  Alert! CPU usage exceeds threshold: {cpu_usage:.1f}%")


def monitor_cpu():
    """
    Main monitoring loop that continuously checks CPU usage.
    """
    print("="*60)
    print("CPU HEALTH MONITORING")
    print("="*60)
    print(f"Threshold: {CPU_THRESHOLD}%")
    print(f"Check Interval: {CHECK_INTERVAL} seconds")
    print(f"Press Ctrl+C to stop monitoring")
    print("="*60)
    print("\nMonitoring CPU usage...\n")
    
    alert_count = 0
    check_count = 0
    
    try:
        while True:
            try:
                # Get CPU usage
                cpu_usage = get_cpu_usage()
                check_count += 1
                
                # Display status and check threshold
                if cpu_usage > CPU_THRESHOLD:
                    alert_count += 1
                
                display_cpu_status(cpu_usage, CPU_THRESHOLD)
                
                # Wait before next check (subtract 1 second used by cpu_percent)
                time.sleep(CHECK_INTERVAL - 1)
                
            except KeyboardInterrupt:
                # Re-raise to handle in outer try-except
                raise
                
            except Exception as e:
                print(f"Error during monitoring: {str(e)}")
                print("Continuing monitoring after error...\n")
                time.sleep(CHECK_INTERVAL)
    
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("MONITORING STOPPED")
        print("="*60)
        print(f"Total checks performed: {check_count}")
        print(f"Total alerts triggered: {alert_count}")
        print("="*60)
        sys.exit(0)
    
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        sys.exit(1)


def main():
    """
    Main entry point for the CPU monitoring script.
    """
    try:
        # Check if psutil is available
        if not hasattr(psutil, 'cpu_percent'):
            raise ImportError("psutil library not properly installed")
        
        # Start monitoring
        monitor_cpu()
        
    except ImportError as e:
        print("Error: psutil library is required.")
        print("Install it using: pip install psutil")
        sys.exit(1)
    
    except Exception as e:
        print(f"Failed to start CPU monitoring: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()