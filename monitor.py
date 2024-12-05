import psutil
import time
import logging

# Initialize logging
logging.basicConfig(filename="monitor_logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

def monitor_cpu_memory():
    """Monitors CPU and memory usage."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    logging.info(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%")
    return {"cpu_usage": cpu_usage, "memory_usage": memory_usage}

def log_request(request_data):
    """Logs details about incoming requests."""
    logging.info(f"Request Details: Method={request_data['method']}, URL={request_data['url']}, "
                 f"Status={request_data['status_code']}, Response Time={request_data['response_time']}")
    return "Request logged."

