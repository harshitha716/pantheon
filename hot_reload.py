import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, process_manager):
        self.process_manager = process_manager
        self.last_modified = time.time()

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            current_time = time.time()
            if current_time - self.last_modified > 1:  # Debounce
                self.last_modified = current_time
                print(f"\n[Hot Reload] File changed: {event.src_path}")
                self.process_manager.restart()


class ProcessManager:
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.start()

    def start(self):
        # print(f"[Hot Reload] Starting process: {' '.join(self.cmd)}")
        self.process = subprocess.Popen(self.cmd)

    def stop(self):
        if self.process:
            # print("[Hot Reload] Stopping process...")
            self.process.terminate()
            self.process.wait()

    def restart(self):
        # print("[Hot Reload] Restarting process...")
        self.stop()
        self.start()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hot_reload.py <script_to_run> [args...]")
        sys.exit(1)

    cmd = [sys.executable] + sys.argv[1:]
    process_manager = ProcessManager(cmd)

    event_handler = ChangeHandler(process_manager)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        process_manager.stop()
    observer.join()
