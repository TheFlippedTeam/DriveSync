import time
from os import walk
from os.path import join
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import drivesync
import ntpath
import logging
import threading

toPerform = []
MAIN_PATH = 'D:\\Scuola\\1_UniVr\\1_Anno\\1S\\Storia'

def map(dir):
    print("Checking: " + dir)
    for(root, dirs, files) in walk(dir, topdown=False):
        for(name) in files:
            print(join(root, name))
        for(name) in dirs:
            print(join(root, name))

def on_created(event):
    print(f"{event.src_path} has been created!")
    toPerform.append(
        [ntpath.basename(event.src_path), event.src_path, "upload"])

def on_deleted(event):
    print(f"{event.src_path} has been deleted!")

def on_modified(event):
    print(f"{event.src_path} has been modified!")
    for action in toPerform:
        if (event.src_path in action) and not("upload" in action):
            toPerform.append(
                [ntpath.basename(event.src_path), event.src_path, "upload"])

    print(toPerform)

def on_moved(event):
    print(f"{event.src_path} has been moved to {event.dest_path}!")
    for action in toPerform:
        if event.src_path in action:
            toPerform.remove(action)

    if MAIN_PATH in event.dest_path:
        toPerform.append([ntpath.basename(event.dest_path),
                          event.dest_path, "upload"])

def observer_thread():
    print("Observer started")
    # Create the Observer
    path = MAIN_PATH
    go_recursively = True
    observer = Observer()
    observer.schedule(event_handler, path, recursive=go_recursively)

    # Start the Observer
    observer.start()
    try:
        while(True):
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

def drivesync_thread():
    print("Drivesync started")
    while(True):
        time.sleep(60 - time.time() % 30)
        # Things to run
        for item in toPerform:
            print(f"Now {item[2]} the file {item[0]} located at {item[1]}")
        toPerform.clear()


if __name__ == "__main__":
    # map("D:\\Scuola\\1_UniVr")

    #DriveApiObj = drivesync.DriveAPI()

    # Create the event handler
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    event_handler = PatternMatchingEventHandler(
        patterns, ignore_patterns, ignore_directories, case_sensitive)

    # Link the event handler to the specific handlers
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved

    observer = threading.Thread(target=observer_thread)
    observer.start()

    drivesync = threading.Thread(target=drivesync_thread)
    drivesync.start()