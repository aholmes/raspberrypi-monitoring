"""
This type stub file was generated by pyright.
"""

MP_METRIC_HELP = ...
class MultiProcessCollector:
    """Collector for files for multi-process mode."""
    def __init__(self, registry, path=...) -> None:
        ...
    
    @staticmethod
    def merge(files, accumulate=...): # -> dict_values[Unknown, Unknown]:
        """Merge metrics from given mmap files.

        By default, histograms are accumulated, as per prometheus wire format.
        But if writing the merged data back to mmap files, use
        accumulate=False to avoid compound accumulation.
        """
        ...
    
    def collect(self): # -> dict_values[Unknown, Unknown]:
        ...
    


def mark_process_dead(pid, path=...): # -> None:
    """Do bookkeeping for when one process dies in a multi-process setup."""
    ...
