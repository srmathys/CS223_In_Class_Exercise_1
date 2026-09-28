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

def bin_search_iter(A,v):
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

    return search(0, len(A) - 1)
