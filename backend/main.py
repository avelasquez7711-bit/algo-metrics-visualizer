import asyncio
import random
import sys
import time
import tracemalloc
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Algorithmic Metrics & Visualizer API")

# data distribution generator ------------------------------
def generate_data(size: int, distribution: str) -> List[int]:
    if distribution == "random":
        return [random.randint(1, 1000) for _ in range(size)]
    elif distribution == "nearly_sorted":
        arr = list(range(1, size + 1))
        swaps = max(1, int(size * 0.05))
        for _ in range(swaps):
            i, j = random.randint(0, size - 1), random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif distribution == "reverse_sorted":
        return list(range(size, 0, -1))
    elif distribution == "few_unique":
        return [random.choice([10, 30, 50, 70, 90]) for _ in range(size)]
    else:
        raise ValueError("Invalid distribution type")


# pure execution engine for benchmarking ----------------------------
def run_benchmark(algorithm: str, distribution: str, size: int) -> Dict[str, Any]:
    arr = generate_data(size, distribution)
    comparisons = 0
    swaps = 0

    tracemalloc.start()
    start_time = time.perf_counter_ns()

    if algorithm == "quick_sort":
        def qs(a, low, high):
            nonlocal comparisons, swaps
            if low < high:
                pivot = a[high]
                i = low - 1
                for j in range(low, high):
                    comparisons += 1
                    if a[j] < pivot:
                        i += 1
                        a[i], a[j] = a[j], a[i]
                        swaps += 1
                a[i + 1], a[high] = a[high], a[i + 1]
                swaps += 1
                p = i + 1
                qs(a, low, p - 1)
                qs(a, p + 1, high)

        sys.setrecursionlimit(max(10000, size * 2))
        qs(arr, 0, len(arr) - 1)

    elif algorithm == "bubble_sort":
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                comparisons += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1

    end_time = time.perf_counter_ns()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    time_ms = round((end_time - start_time) / 1e6, 3)
    peak_mem_kb = round(peak_mem / 1024, 2)

    return {
        "algorithm": algorithm,
        "distribution": distribution,
        "dataset_size": size,
        "time_ms": time_ms,
        "comparisons": comparisons,
        "swaps": swaps,
        "peak_memory_kb": peak_mem_kb,
    }

