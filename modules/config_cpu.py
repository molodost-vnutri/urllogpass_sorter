import psutil

class ConfigCpu:
    def __init__(self, thread_auto: bool, threads: int) -> int:
        self.threads: int = threads
        if thread_auto:
            self.threads: int = psutil.cpu_count(logical=True) - 1
        
    def get(self):
        return int(self.threads)