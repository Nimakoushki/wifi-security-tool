import sys
import signal
import atexit
import json
import os
from datetime import datetime

class ExitHandler:
    def __init__(self):
        self.active_processes = []
        self.save_state_on_exit = True
        self.state_file = "wifi_tool_state.json"
        self.is_exiting = False
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        atexit.register(self.cleanup)
        print("[OK] ExitHandler initialized")

    def register_process(self, process, name="Unknown"):
        self.active_processes.append({"process": process, "name": name})

    def save_state(self, data=None):
        if not self.save_state_on_exit:
            return
        state = {"timestamp": datetime.now().isoformat(), "data": data if data else {}}
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            print(f"[SAVED] State saved to {self.state_file}")
        except Exception as e:
            print(f"[ERROR] Failed to save state: {e}")

    def load_state(self):
        if not os.path.exists(self.state_file):
            return None
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f).get("data", {})
        except:
            return None

    def signal_handler(self, signum, frame):
        print(f"\n[SIGNAL] Received signal {signum}. Exiting gracefully...")
        self.cleanup()
        sys.exit(0)

    def kill_all_processes(self):
        for proc in self.active_processes:
            try:
                if proc["process"].poll() is None:
                    proc["process"].terminate()
                    print(f"[STOP] Terminated: {proc['name']}")
            except:
                pass
        self.active_processes.clear()

    def cleanup(self):
        if self.is_exiting:
            return
        self.is_exiting = True
        print("\n[CLEANUP] Cleaning up...")
        self.kill_all_processes()
        print("[CLEANUP] Done.")