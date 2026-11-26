"""Educational implementations of nine sorting algorithms.

Every public function accepts a list of integers and returns a sorted copy.
The input list is never modified.
"""


def selection_sort(numbers: list[int]) -> list[int]:
    arr = numbers.copy()
    n = len(arr)

    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr


def insertion_sort(numbers: list[int]) -> list[int]:
    arr = numbers.copy()

    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > current:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current

    return arr


def merge_sort(numbers: list[int]) -> list[int]:
    if len(numbers) <= 1:
        return numbers.copy()

    mid = len(numbers) // 2
    left = merge_sort(numbers[:mid])
    right = merge_sort(numbers[mid:])

    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(numbers: list[int]) -> list[int]:
    if len(numbers) <= 1:
        return numbers.copy()

    pivot = numbers[len(numbers) // 2]
    left = [x for x in numbers if x < pivot]
    equal = [x for x in numbers if x == pivot]
    right = [x for x in numbers if x > pivot]

    return quick_sort(left) + equal + quick_sort(right)


def heap_sort(numbers: list[int]) -> list[int]:
    arr = numbers.copy()
    n = len(arr)

    def sift_down(root: int, end: int) -> None:
        while 2 * root + 1 <= end:
            child = 2 * root + 1
            if child + 1 <= end and arr[child] < arr[child + 1]:
                child += 1
            if arr[root] >= arr[child]:
                break
            arr[root], arr[child] = arr[child], arr[root]
            root = child

    for start in range(n // 2 - 1, -1, -1):
        sift_down(start, n - 1)

    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        sift_down(0, end - 1)

    return arr


def counting_sort(numbers: list[int]) -> list[int]:
    if not numbers:
        return []

    minimum = min(numbers)
    maximum = max(numbers)
    counts = [0] * (maximum - minimum + 1)

    for value in numbers:
        counts[value - minimum] += 1

    result = []
    for offset, count in enumerate(counts):
        result.extend([minimum + offset] * count)
    return result


def bucket_sort(numbers: list[int]) -> list[int]:
    if len(numbers) <= 1:
        return numbers.copy()

    minimum = min(numbers)
    maximum = max(numbers)
    if minimum == maximum:
        return numbers.copy()

    n = len(numbers)
    buckets = [[] for _ in range(n)]
    for value in numbers:
        index = (value - minimum) * (n - 1) // (maximum - minimum)
        buckets[index].append(value)

    result = []
    for bucket in buckets:
        result.extend(insertion_sort(bucket))
    return result


def radix_sort(numbers: list[int]) -> list[int]:
    def sort_nonnegative(values: list[int]) -> list[int]:
        if not values:
            return []

        arr = values.copy()
        maximum = max(arr)
        place = 1

        while maximum // place > 0:
            counts = [0] * 10
            for value in arr:
                counts[(value // place) % 10] += 1

            for i in range(1, 10):
                counts[i] += counts[i - 1]

            result = [0] * len(arr)
            for value in reversed(arr):
                digit = (value // place) % 10
                counts[digit] -= 1
                result[counts[digit]] = value

            arr = result
            place *= 10

        return arr

    negatives = [-value for value in numbers if value < 0]
    nonnegatives = [value for value in numbers if value >= 0]

    sorted_negatives = sort_nonnegative(negatives)
    sorted_nonnegatives = sort_nonnegative(nonnegatives)
    return [-value for value in reversed(sorted_negatives)] + sorted_nonnegatives


def tim_sort(numbers: list[int]) -> list[int]:
    """Simplified educational TimSort: natural runs + minrun + run merging.

    Does not implement CPython TimSort's galloping optimizations.
    """
    arr = numbers.copy()
    n = len(arr)
    if n <= 1:
        return arr

    def min_run_length(size: int) -> int:
        remainder = 0
        while size >= 64:
            remainder |= size & 1
            size >>= 1
        return size + remainder

    def extend_run(start: int, sorted_end: int, end: int) -> None:
        for i in range(sorted_end, end):
            current = arr[i]
            j = i - 1
            while j >= start and arr[j] > current:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = current

    runs: list[tuple[int, int]] = []

    def merge_at(index: int) -> None:
        left_start, left_length = runs[index]
        right_start, right_length = runs[index + 1]
        left = arr[left_start:left_start + left_length]
        right = arr[right_start:right_start + right_length]

        i = j = 0
        write = left_start
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[write] = left[i]
                i += 1
            else:
                arr[write] = right[j]
                j += 1
            write += 1

        arr[write:write + len(left) - i] = left[i:]
        write += len(left) - i
        arr[write:write + len(right) - j] = right[j:]
        runs[index:index + 2] = [(left_start, left_length + right_length)]

    minimum_run = min_run_length(n)
    start = 0

    while start < n:
        end = start + 1
        if end < n and arr[end] < arr[start]:
            while end < n and arr[end] < arr[end - 1]:
                end += 1
            arr[start:end] = reversed(arr[start:end])
        else:
            while end < n and arr[end] >= arr[end - 1]:
                end += 1

        forced_end = min(n, start + max(minimum_run, end - start))
        extend_run(start, end, forced_end)
        runs.append((start, forced_end - start))

        while len(runs) > 1:
            count = len(runs)
            if count >= 3 and runs[-3][1] <= runs[-2][1] + runs[-1][1]:
                merge_at(count - 3 if runs[-3][1] < runs[-1][1] else count - 2)
            elif runs[-2][1] <= runs[-1][1]:
                merge_at(count - 2)
            else:
                break

        start = forced_end

    while len(runs) > 1:
        merge_at(len(runs) - 2)

    return arr


if __name__ == "__main__":
    sample = [5, -2, 9, 1, 5, 0, -7]
    algorithms = [
        selection_sort, insertion_sort, merge_sort, quick_sort, heap_sort,
        counting_sort, bucket_sort, radix_sort, tim_sort,
    ]
    for algorithm in algorithms:
        print(f"{algorithm.__name__}: {algorithm(sample)}")
