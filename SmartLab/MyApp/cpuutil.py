import psutil
import threading
import time
import requests

ip="127.0.0.1:8000"
def get_memory_info(system):
    mem = psutil.virtual_memory()
    try:
     while True:
        a=system
        tm=f"{mem.total / (1024**3):.2f} GB"
        am=f"{mem.available / (1024**3):.2f} GB"
        um=f"{mem.used / (1024**3):.2f} GB"
        mu=f"{mem.percent}%"
        requests.get("http://"+ip+"/insert_memory?id="+str(a)+"&tm="+str(tm)+"&am="+am+"&um="+um+"&mu="+mu)
        mem = psutil.virtual_memory()
        print(f"Total Memory: {mem.total / (1024**3):.2f} GB")
        print(f"Available Memory: {mem.available / (1024**3):.2f} GB")
        print(f"Used Memory: {mem.used / (1024**3):.2f} GB")
        print(f"Memory Utilization: {mem.percent}%")
        time.sleep(5)  # Sleep for 5 seconds before printing againt
    except Exception as e:
        print(e,"hhhhhhhhhhhhhhhhhhh")

if __name__ == "__main__":
    # Run get_memory_info in a background thread
    memory_thread = threading.Thread(target=get_memory_info, daemon=True)
    memory_thread.start()
