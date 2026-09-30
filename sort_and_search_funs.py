#  coding: utf-8
# Sort and search functions
def insert_sort_iter(A):

def insert_sort_rec(A):

def select_sort_iter(A):

def select_sort_rec(A):

def merge_sort_iter(A):

def merge_sort_rec(A):

def quick_sort_iter(A):

def quick_sort_rec(A):

'''def bin_search_iter(A,v):
  """Return the index of v in sorted list A, or None if v is absent."""
    low = 0
    high = len(A) - 1

    while low <= high:
        mid = (low + high) // 2

        if A[mid] == v:
            return mid
        elif A[mid] < v:
            low = mid + 1
        else:
            high = mid - 1

    return None

def bin_search_rec(A,v):
  """Return the index of v in sorted list A, or None if v is absent."""

    def search(low, high):
        if low > high:
            return None

        mid = (low + high) // 2

        if A[mid] == v:
            return mid
        elif A[mid] < v:
            return search(mid + 1, high)
        else:
            return search(low, mid - 1)

    return search(0, len(A) - 1)'''
### Search Algorithms ###

@ timer_decorator
def binary_search_iter(A, col=0, value=None, asc=True, bound=None):
    # Goal: Search a sorted DataFrame column using iterative binary search.
    # A: DataFrame to search
    # col: column position used for comparison
    # value: value being searched for
    # asc: True for ascending order; False for descending order
    # bound: None, "lower", or "upper"

    # Obtain the number of rows in the DataFrame.
    length = A.iloc[:, col].size

    # Set the initial search boundaries.
    low = 0
    high = length - 1
    result = None

    # Continue while the search interval is not empty.
    while low <= high:

        # Find the middle row.
        mid = (low + high) // 2
        current_value = A.iat[mid, col]

        if bound == "lower":

            # Find the first value greater than or equal to value
            # when the column is sorted in ascending order.
            if asc and current_value >= value:
                result = mid
                high = mid - 1

            # Find the first value less than or equal to value
            # when the column is sorted in descending order.
            elif not asc and current_value <= value:
                result = mid
                high = mid - 1
            else:
                low = mid + 1

        elif bound == "upper":

            # Find the first value greater than value
            # when the column is sorted in ascending order.
            if asc and current_value > value:
                result = mid
                high = mid - 1

            # Find the first value less than value
            # when the column is sorted in descending order.
            elif not asc and current_value < value:
                result = mid
                high = mid - 1
            else:
                low = mid + 1

        else:

            # Return the index when an exact match is found.
            if current_value == value:
                return mid

            # For ascending data, search the right half
            # when the middle value is too small.
            if asc and current_value < value:
                low = mid + 1

            # For descending data, search the right half
            # when the middle value is too large.
            elif not asc and current_value > value:
                low = mid + 1

            # Otherwise, search the left half.
            else:
                high = mid - 1

    # Return the closest bound position when requested.
    if bound in ("lower", "upper"):
        return low if result is None else result

    # Return None when an exact match was not found.
    return None


@ timer_decorator
def binary_search_rec(A, col=0, value=None, low=0, high=None, asc=True, bound=None):
    # Goal: Search a sorted DataFrame column using recursive binary search.
    # A: DataFrame to search
    # col: column position used for comparison
    # value: value being searched for
    # low and high: boundaries of the current search interval
    # asc: True for ascending order; False for descending order
    # bound: None, "lower", or "upper"

    # Set high to the final row during the first function call.
    if high is None:
        high = A.iloc[:, col].size - 1

    # Base case: the search interval is empty.
    if low > high:

        # For a bound search, low is the closest insertion position.
        if bound in ("lower", "upper"):
            return low

        # For an exact search, return None if value is absent.
        return None

    # Find the middle row.
    mid = (low + high) // 2
    current_value = A.iat[mid, col]

    if bound == "lower":

        # Search left for an earlier valid lower-bound position.
        if asc and current_value >= value:
            return binary_search_rec(A, col, value, low, mid - 1, asc, bound)

        if not asc and current_value <= value:
            return binary_search_rec(A, col, value, low, mid - 1, asc, bound)

        # Otherwise, search the right half.
        return binary_search_rec(A, col, value, mid + 1, high, asc, bound)

    elif bound == "upper":

        # Search left for an earlier valid upper-bound position.
        if asc and current_value > value:
            return binary_search_rec(A, col, value, low, mid - 1, asc, bound)

        if not asc and current_value < value:
            return binary_search_rec(A, col, value, low, mid - 1, asc, bound)

        # Otherwise, search the right half.
        return binary_search_rec(A, col, value, mid + 1, high, asc, bound)

    else:

        # Return the index when an exact match is found.
        if current_value == value:
            return mid

        # For ascending data, search right when current_value is too small.
        if asc and current_value < value:
            return binary_search_rec(A, col, value, mid + 1, high, asc, bound)

        # For descending data, search right when current_value is too large.
        if not asc and current_value > value:
            return binary_search_rec(A, col, value, mid + 1, high, asc, bound)

        # Otherwise, search the left half.
        return binary_search_rec(A, col, value, low, mid - 1, asc, bound)
