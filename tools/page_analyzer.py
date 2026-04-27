import sys
import re

def analyze_logs(log_path):
    print(f"Analyzing CHUNK logs: {log_path}")
    
    faults = 0
    prefetches = 0
    hits = 0
    
    try:
        with open(log_path, "r") as f:
            for line in f:
                if "page fault" in line.lower():
                    faults += 1
                if "prefetch" in line.lower():
                    prefetches += 1
                if "hit" in line.lower():
                    hits += 1
    except FileNotFoundError:
        print("Log file not found.")
        return

    print("--- Performance Report ---")
    print(f"Total Page Faults: {faults}")
    print(f"Total Prefetches:  {prefetches}")
    if prefetches > 0:
        print(f"Hit Rate:          {(hits/prefetches)*100:.2f}%")
    print("--------------------------")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python page_analyzer.py <log_file>")
    else:
        analyze_logs(sys.argv[1])
