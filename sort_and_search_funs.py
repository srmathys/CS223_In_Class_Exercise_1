#  coding: utf-8
# Sort and search functions
import pandas as pd
from util_funs import timer_decorator
import sys

# note: A.iat gets a single value using integer positioning in pandas
@ timer_decorator
def insert_sort_iter(A,col,asc = True): #A is a dataframe, col is number
    n = len(A)
    if n <= 1:
        return

    index_guide = list(range(n))
    # Shifting values in a premade list in order to track where insertions are happening

    for i in range(1,n):
        j = i - 1
        key = index_guide[i]
        if asc == True:
            while j >= 0 and A.iat[i,col] < A.iat[index_guide[j],col]:
                index_guide[j+1] = index_guide[j] #if key is less than swap
                j -= 1
            index_guide[j + 1] = key
        else:
            while j >= 0 and A.iat[i, col] > A.iat[index_guide[j], col]:
                index_guide[j + 1] = index_guide[j]  # if key is less than swap
                j -= 1
            index_guide[j + 1] = key
    # Reorder the
    A.iloc[:] = A.iloc[index_guide].values


@timer_decorator
def insert_sort_rec(A, col, n=None, index_guide = None, asc=True):

    if n is None:
        n = len(A) # allows for dynamic sizing
    if index_guide is None:
        index_guide = list(range(n))
    if n <= 1:
        return  index_guide
    # start recursions
    # sending an index guide to do the final swap only once.
    index_guide = insert_sort_rec(A, col, n = n - 1, index_guide = index_guide, asc= asc)
    key_index = index_guide[n-1]
    key_val = A.iat[key_index,col]
    j = n - 2

    if asc == True:
        while j >= 0 and key_val < A.iat[index_guide[j], col]:
            index_guide[j + 1] = index_guide[j]  # if key is less than swap
            j -= 1

    else:
        while j >= 0 and key_val > A.iat[index_guide[j], col]:
            index_guide[j + 1] = index_guide[j]  # if key is less than swap
            j -= 1
    index_guide[j + 1] = key_index
## only swaps at end
    if n == len(A):
        A[:] = A.iloc[index_guide].values
    return index_guide # So that it's using the same guide for the entire time




@timer_decorator
def selection_sort_iter(A,col = 0,asc = True):
 
    # Goal: Sorting a DataFrame using iterative selection sort.
    # A: DataFrame to sort
    # col: column position used for comparison
    # asc: should be True for ascending order, False for descending order

    # Obtain the number of rows in the DataFrame
    length = A.iloc[:,col].size
    if asc == True:
        # Process every position except the final one
        # The final element should be in the correct position
        for i in range(length -1):
            # finding the minimum element in the unsorted sublist from a dataframe column
            # once found, it can be swapped with the index of i
            
            # Assume that the first element in the unsorted portion is the smallest element.
            min = i

            # Search the remaining unsorted portion of the column. 
            for j in range(i+1,length):

                # Update the min if a smaller value is found.
                if A.iat[j,col] < A.iat[min,col]:
                    min = j
            # Exchange the selected minimum row with row i
            # Entire row is exchanged, not just the selected column
            A.iloc[[i,min]] = A.iloc[[min,i]].values
    else:
        # Descending-order version searches for the maximum.
        for i in range(length - 1): #same thing, but with max
            # Assume the first element in the unsorted portion is the largest element.
            max = i

            # Search the remaining unsorted portion of the column.
            for j in range(i+1,length):

                # Update the max if a larger value is found. 
                if A.iat[j,col] > A.iat[max,col]:
                    max = j
            # Exchange the selected maximum row with row i
            A.iloc[[i,max]] = A.iloc[[max,i]].values

@ timer_decorator
def selection_sort_rec(A,col = 0,asc = True, i = 0):
    length = A.iloc[:,col].size
    if asc == True:
        min = i
        for j in range(i + 1, length):
            if A.iat[j, col] < A.iat[min, col]:
                min = j
        A.iloc[[i, min]] = A.iloc[[min, i]].values

        if i+1 < length:
            selection_sort_rec(A,col, asc = True, i = i+1)
    else:
        max = i
        for j in range(i + 1, length):
            if A.iat[j, col] > A.iat[max, col]:
                max = j
        A.iloc[[i, max]] = A.iloc[[max, i]].values
        if i+1 < length:
            selection_sort_rec(A,col, asc = False, i = i+1)


### Helper functions for Quicksort ###
def median_of_three(A, col, low, high, asc = True):
    #### Using Median of Three instead of Lomuto Partitioning ###
    mid = low + (high - low) // 2
    # sorting the low, mid and high positions in place
    if asc == True:
        if A.iat[high,col] < A.iat[low,col]:
            A.iloc[[low, high]] = A.iloc[[high, low]].values
        if A.iat[mid,col] < A.iat[low,col]:
            A.iloc[[low, mid]] = A.iloc[[mid, low]].values
        if A.iat[high,col] < A.iat[mid,col]:
            A.iloc[[mid,high]] = A.iloc[[high, mid]].values
        A.iloc[[mid,high]] = A.iloc[[high, mid]].values
        return A.iat[high,col]
    else:
        if A.iat[high,col] > A.iat[low,col]:
            A.iloc[[low, high]] = A.iloc[[high, low]].values
        if A.iat[mid,col] > A.iat[low,col]:
            A.iloc[[low, mid]] = A.iloc[[mid, low]].values
        if A.iat[high,col] > A.iat[mid,col]:
            A.iloc[[mid,high]] = A.iloc[[high, mid]].values
        A.iloc[[mid,high]] = A.iloc[[high, mid]].values
        return A.iat[high,col]

def partition(A, col, low, high, asc = True):
    ### Helper for Quicksort on partitioning ###
    pivot_val = median_of_three(A,col, low, high, asc)
    i = low - 1
    if asc == True:
        for j in range(low, high):
            if A.iat[j,col] <= pivot_val:
                i += 1
                A.iloc[[i,j]] = A.iloc[[j,i]].values
        A.iloc[[i+1,high]] = A.iloc[[high, i+1]].values
        return i + 1
    else:
        for j in range(low, high):
            if A.iat[j,col] >= pivot_val:
                i += 1
                A.iloc[[i, j]] = A.iloc[[j, i]].values
        A.iloc[[i + 1, high]] = A.iloc[[high, i + 1]].values
        return i + 1

@ timer_decorator
def quick_sort_iter(A ,col, asc = True):
#Iterative sorting using quicksort
    low = 0
    high = A.iloc[:,col].size -1

    #### Creating initial stack size
    size = high - low + 1
    stack = [0]*size

    ### pushing initial values into the stack
    stack[0] = low
    stack[1]= high
    top = 1

    while top >= 0:
        ### setting this back
        high = stack[top]
        low = stack[top -1]
        top-=2

        if low < high:
            #
            p = partition(A, col, low, high, asc)
    # Try to grab the larger size of the partition to deal with first
            left_side_size = p - 1 - low
            right_side_size = high - p + 1

            if left_side_size > right_side_size:
    # This means left is the bigger side of the partition
                if p - 1 > low:
                    top += 1; stack[top] = low
                    top += 1; stack[top] = p -1
                if p + 1 < high:
                    top += 1; stack[top] = p + 1
                    top += 1; stack[top] = high
            else:
    # This means right side is bigger or they are the same size
                if p + 1 < high:
                    top += 1; stack[top] = p + 1
                    top += 1; stack[top] = high
                if p-1 > low:
                    top += 1; stack[top] = low
                    top += 1; stack[top] = p - 1


@ timer_decorator
def quick_sort_rec(A,col,low = 0, high = None ,asc = True):
    if high is None:
        high = A.iloc[:,col].size -1
    if low < high:
        pivot_loc = partition(A, col, low, high, asc)

        quick_sort_rec(A,col,low, pivot_loc-1, asc)
        quick_sort_rec(A,col,pivot_loc+1, high, asc)

# Merge Sort Helper Function

def merge(A: pd.DataFrame, col: int, left: int, middle: int, right: int, asc=True):
    n1 = middle - left + 1
    n2 = right - middle

    # Use .copy() so changes to A don't alter these mid-operation
    left_array = A.iloc[left: left + n1].copy()
    right_array = A.iloc[middle + 1: middle + 1 + n2].copy()

    i = j = 0
    k = left

    while i < n1 and j < n2:
        val_left = left_array.iloc[i, col]
        val_right = right_array.iloc[j, col]

        # Handle ascending vs descending comparison
        condition = (val_left <= val_right) if asc else (val_left >= val_right)

        if condition:
            A.iloc[k] = left_array.iloc[i]
            i += 1
        else:
            A.iloc[k] = right_array.iloc[j]
            j += 1
        k += 1

    while i < n1:
        A.iloc[k] = left_array.iloc[i]
        i += 1
        k += 1

    while j < n2:
        A.iloc[k] = right_array.iloc[j]
        j += 1
        k += 1

@ timer_decorator
def merge_sort_iter(A: pd.DataFrame, col: int, asc=True):
    n = len(A)
    curr_size = 1

    while curr_size < n:
        left_start = 0
        while left_start < n - 1:
            mid = min(left_start + curr_size - 1, n - 1)
            right_end = min(left_start + 2 * curr_size - 1, n - 1)

            # Pass col and asc down to the merge function
            merge(A, col, left_start, mid, right_end, asc)
            left_start += 2 * curr_size

        curr_size *= 2

@ timer_decorator
def merge_sort_rec(A: pd.DataFrame, col: int, asc: bool = True):
    if len(A) <= 1:
        return A

    #split array in half
    mid = len(A) // 2
    left_half = A.iloc[:mid]
    right_half = A.iloc[mid:]

    merge_sort_rec(left_half, col, asc)
    merge_sort_rec(right_half, col, asc)

    i = j = k = 0

    #recursively sorting
    while i < len(left_half) and j < len(right_half):
        left_val = left_half.iat[i, col]
        right_val = right_half.iat[j, col]

        if (asc and left_val <= right_val) or (not asc and left_val >= right_val):
            A.iloc[k] = left_half.iloc[i].values
            i += 1
        else:
            A.iloc[k] = right_half.iloc[j].values
            j += 1
        k += 1

    while i < len(left_half):
        A.iloc[k] = left_half.iloc[i].values
        i += 1
        k += 1

    while j < len(right_half):
        A.iloc[k] = right_half.iloc[j].values
        j += 1
        k += 1

    return A
### Search Algorithms ###

def bin_search_iter(A,v):
  ###Return the index of v in sorted list A, or None if v is absent."""
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
  ###Return the index of v in sorted list A, or None if v is absent."""

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








if __name__ == "__main__":
    print("<module name> : Is intended to be imported and not executed.")
