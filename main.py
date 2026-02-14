import time
import sys
import random


# ==============================
# PERFORMANCE TRACKER
# ==============================
class PerformanceTracker:
    def __init__(self):
        self.comparisons = 0

    def reset(self):
        self.comparisons = 0


# ==============================
# QUICK SORT
# ==============================
def quick_sort(arr, tracker):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    left = []
    middle = []
    right = []

    for x in arr:
        tracker.comparisons += 1
        if x < pivot:
            left.append(x)
        elif x > pivot:
            right.append(x)
        else:
            middle.append(x)

    return quick_sort(left, tracker) + middle + quick_sort(right, tracker)


# ==============================
# MERGE SORT
# ==============================
def merge_sort(arr, tracker):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], tracker)
    right = merge_sort(arr[mid:], tracker)

    return merge(left, right, tracker)


def merge(left, right, tracker):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        tracker.comparisons += 1
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


# ==============================
# ANALYSIS FUNCTION
# ==============================
def analyze_algorithm(algorithm, data):
    tracker = PerformanceTracker()
    data_copy = data.copy()

    start_time = time.time()
    sorted_data = algorithm(data_copy, tracker)
    end_time = time.time()

    execution_time = end_time - start_time
    memory_used = sys.getsizeof(sorted_data)

    return {
        "sorted_data": sorted_data,
        "time": execution_time,
        "comparisons": tracker.comparisons,
        "memory": memory_used
    }


# ==============================
# MAIN SYSTEM FLOW
# ==============================
def main():
    print("====== SMART SORTING SYSTEM ======\n")

    # INPUT PHASE
    data = input("Enter numbers separated by commas: ")
    try:
        data_array = list(map(int, data.split(",")))
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return

    print("\n--- SELECTION PHASE ---")
    print("System will run BOTH Quick Sort and Merge Sort for comparison.\n")

    # PROCESSING & ANALYSIS PHASE
    quick_result = analyze_algorithm(quick_sort, data_array)
    merge_result = analyze_algorithm(merge_sort, data_array)

    # OUTPUT PHASE
    print("====== SORTED OUTPUT ======")
    print("Sorted Data:", quick_result["sorted_data"])

    print("\n====== PERFORMANCE REPORT ======")

    print("\nQuick Sort:")
    print("Time:", round(quick_result["time"], 6), "seconds")
    print("Comparisons:", quick_result["comparisons"])
    print("Memory Used:", quick_result["memory"], "bytes")

    print("\nMerge Sort:")
    print("Time:", round(merge_result["time"], 6), "seconds")
    print("Comparisons:", merge_result["comparisons"])
    print("Memory Used:", merge_result["memory"], "bytes")

    print("\n====== DECISION INSIGHT ======")

    if quick_result["time"] < merge_result["time"]:
        print("Quick Sort was faster for this dataset.")
    else:
        print("Merge Sort was faster for this dataset.")

    print("Use this insight to optimize future sorting tasks.")


if __name__ == "__main__":
    main()