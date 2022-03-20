import os
import json
import shutil

from threading import Thread

class Cleaner(Thread):
    
    def __init__(self):
        
        self.local = os.getenv("LOCALAPPDATA")
        self.roaming = os.getenv("APPDATA")
        
        with open("path.json") as r:
            self.paths = json.load(r)[-1]
            
    def run(self):
        for path in self.paths:
            for name, cache_paths in self.paths[path].items():
                print(f"Cleaning {name} in {path.capitalize()} Appdata")
                for cache_path in cache_paths:
                    if cache_path:
                        if path == "local":
                            folder = self.local + cache_path
                        elif path == "roaming":
                            folder = self.roaming + cache_path
                        for filename in os.listdir(folder):
                            file_path = os.path.join(folder, filename)
                            try:
                                if os.path.isfile(file_path) or os.path.islink(file_path):
                                    os.unlink(file_path)
                                elif os.path.isdir(file_path):
                                    shutil.rmtree(file_path)
                            except Exception:
                                print("Failed to delete " + file_path)
                            else:
                                print("Successfully deleted " + file_path)
        
        
if __name__ == "__main__":
    Cleaner().run()