from psutil import cpu_count

from modules.file import config

def cpu_config() -> int:
    if config.thread_auto:
        return cpu_count(logical=True) - 1
    return config.threads

logical_core = cpu_config()