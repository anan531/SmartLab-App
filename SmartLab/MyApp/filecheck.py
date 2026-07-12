import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Define the event handler class
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f'File modified: {event.src_path}')

    def on_created(self, event):
        if not event.is_directory:
            print(f'File created: {event.src_path}')

    def on_deleted(self, event):
        if not event.is_directory:
            print(f'File deleted: {event.src_path}')

    def on_moved(self, event):
        if not event.is_directory:
            print(f'File moved from {event.src_path} to {event.dest_path}')


# Specify the directory you want to monitor
directory_to_monitor = "D:\\"  # Change this to your target directory

# Set up the observer and event handler
event_handler = FileChangeHandler()
observer = Observer()
observer.schedule(event_handler, path=directory_to_monitor, recursive=False)

# Start monitoring the directory
print(f"Monitoring changes in directory: {directory_to_monitor}")
observer.start()

try:
    while True:
        time.sleep(1)  # Keeps the program running to continue monitoring
except KeyboardInterrupt:
    print("Monitoring stopped.")
    observer.stop()

# Wait for the observer to finish
observer.join()