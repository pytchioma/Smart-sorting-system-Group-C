"""
SMART SORTING BENCHMARK SYSTEM
--------------------------------
This program compares two sorting approaches:

1. In-place Quick Sort
2. Merge Sort

It measures:
- Execution time
- Number of comparisons
- Deep memory usage

Supported data types:
- Numbers
- Strings
- Custom objects (Person class)
"""

import time
import sys


# ==========================================================
# PERFORMANCE TRACKER CLASS
# ==========================================================
class PerformanceTracker:
    """
    Tracks algorithm performance metrics.
    Currently tracks:
    - Number of element comparisons
    """

    def __init__(self):
        self.comparisons = 0

    def reset(self):
        self.comparisons = 0


# ==========================================================
# DEEP MEMORY SIZE CALCULATION
# ==========================================================
def deep_getsizeof(obj, seen=None):
    """
    Recursively calculates the total memory footprint of an object.
    Fixes the limitation of sys.getsizeof() which only measures shallow size.
    """

    size = sys.getsizeof(obj)

    if seen is None:
        seen = set()

    obj_id = id(obj)

    if obj_id in seen:
        return 0

    seen.add(obj_id)

    if isinstance(obj, dict):
        size += sum(
            deep_getsizeof(k, seen) + deep_getsizeof(v, seen)
            for k, v in obj.items()
        )

    elif hasattr(obj, "__dict__"):
        size += deep_getsizeof(obj.__dict__, seen)

    elif isinstance(obj, (list, tuple, set)):
        size += sum(deep_getsizeof(i, seen) for i in obj)

    return size


# ==========================================================
# IN-PLACE QUICK SORT
# ==========================================================
def quick_sort(arr, tracker, key=lambda x: x, reverse=False):
    """
    In-place Quick Sort using Lomuto partition scheme.
    """

    def partition(low, high):
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            tracker.comparisons += 1

            if reverse:
                condition = key(arr[j]) > key(pivot)
            else:
                condition = key(arr[j]) < key(pivot)

            if condition:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def _quick_sort(low, high):
        if low < high:
            pi = partition(low, high)
            _quick_sort(low, pi - 1)
            _quick_sort(pi + 1, high)

    _quick_sort(0, len(arr) - 1)
    return arr


# ==========================================================
# MERGE SORT
# ==========================================================
def merge_sort(arr, tracker, key=lambda x: x, reverse=False):
    """
    Merge Sort algorithm (Divide and Conquer).
    Always O(n log n).
    """

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = merge_sort(arr[:mid], tracker, key, reverse)
    right = merge_sort(arr[mid:], tracker, key, reverse)

    return merge(left, right, tracker, key, reverse)


def merge(left, right, tracker, key, reverse):
    """
    Merges two sorted lists into a single sorted list.
    """

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        tracker.comparisons += 1

        if reverse:
            condition = key(left[i]) > key(right[j])
        else:
            condition = key(left[i]) < key(right[j])

        if condition:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


# ==========================================================
# ANALYSIS FUNCTION
# ==========================================================
def analyze_algorithm(algorithm, data, key=lambda x: x, reverse=False):
    """
    Runs a sorting algorithm and measures:
    - Execution time
    - Comparison count
    - Deep memory usage
    """

    tracker = PerformanceTracker()
    data_copy = data.copy()

    start_time = time.time()
    sorted_data = algorithm(data_copy, tracker, key, reverse)
    end_time = time.time()

    return {
        "sorted_data": sorted_data,
        "time": end_time - start_time,
        "comparisons": tracker.comparisons,
        "memory": deep_getsizeof(sorted_data),
    }


# ==========================================================
# MAIN PROGRAM
# ==========================================================
def main():

    print("====== SMART SORTING BENCHMARK SYSTEM ======\n")

    print("Select Data Type:")
    print("1 - Numbers")
    print("2 - Strings")
    print("3 - Objects")

    choice = input("Enter choice: ")

    # ------------------------------
    # NUMBERS
    # ------------------------------
    if choice == "1":
        data = input("Enter numbers separated by commas: ")
        data_array = [float(x.strip()) for x in data.split(",")]
        key_function = lambda x: x

    # ------------------------------
    # STRINGS
    # ------------------------------
    elif choice == "2":
        data = input("Enter words separated by commas: ")
        data_array = [x.strip() for x in data.split(",")]
        key_function = lambda x: x.lower()

    # ------------------------------
    # OBJECTS
    # ------------------------------
    elif choice == "3":

        class Person:
            def __init__(self, name, age, grade):
                self.name = name
                self.age = age
                self.grade = grade

            def __repr__(self):
                return f"{self.name} | Age: {self.age} | Grade: {self.grade}"

        count = int(input("How many people? "))
        data_array = []

        for _ in range(count):
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            grade = float(input("Enter grade: "))
            data_array.append(Person(name, age, grade))

        print("\nSort By:")
        print("1 - Age")
        print("2 - Name")
        print("3 - Grade")
        print("4 - Age then Name")
        print("5 - Grade then Age")

        sort_choice = input("Choose sorting strategy: ")

        if sort_choice == "1":
            key_function = lambda p: p.age
        elif sort_choice == "2":
            key_function = lambda p: p.name.lower()
        elif sort_choice == "3":
            key_function = lambda p: p.grade
        elif sort_choice == "4":
            key_function = lambda p: (p.age, p.name.lower())
        elif sort_choice == "5":
            key_function = lambda p: (p.grade, p.age)
        else:
            print("Invalid choice.")
            return

    else:
        print("Invalid choice.")
        return

    # ------------------------------
    # SORT DIRECTION
    # ------------------------------
    print("\nSort Direction:")
    print("1 - Ascending")
    print("2 - Descending")

    direction_choice = input("Choose direction: ")
    reverse = True if direction_choice == "2" else False

    print("\nRunning Quick Sort and Merge Sort...\n")

    quick_result = analyze_algorithm(quick_sort, data_array, key_function, reverse)
    merge_result = analyze_algorithm(merge_sort, data_array, key_function, reverse)

    # ------------------------------
    # OUTPUT
    # ------------------------------
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

    # ------------------------------
    # DECISION INSIGHT
    # ------------------------------
    print("\n====== DECISION INSIGHT ======")

    if quick_result["time"] < merge_result["time"]:
        print("Quick Sort was faster for this dataset.")
    else:
        print("Merge Sort was faster for this dataset.")


# ==========================================================
# ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    main()
