#  coding: utf-8
# Sort and search functions
import pandas as pd
from util_funs import timer_decorator
import sys

##########################################
##       SORT FUNCTIONS                 ##
##     For Use with Dataframe Objects   ##
##     Fitted with Timer Decorators     ##
##########################################
# Note: timer_decorator currently optimized to return value

@ timer_decorator
def insert_sort_iter(A,col,asc = True): 
    # Goal: Sorting DataFrame using iterative insert sort
    # A: DataFrame to sort
    # col: column position used for comparison
    # asc: should be True for ascending order, False for descending order

    # Store the number of rows in the DataFrame
    n = len(A)

    # DataFrame with 0 or 1 is already sorted. 
    if n <= 1:
        return
    # Create a list of row indices
    # DataFrame rows are not moved during the sorting process
    index_guide = list(range(n))
    # Shifting values in a premade list to track where insertions are happening

    # Begin at the second row because the first row is already sorted.
    for i in range(1,n):
        # Compare the current row with the row before it. 
        j = i - 1
        # Store the index of the row being inserted.
        key = index_guide[i]
        if asc == True:
            # Shift the indices to the right while the value of the key is smaller than the value in the sorted portion.
            while j >= 0 and A.iat[i,col] < A.iat[index_guide[j],col]:
                # Shift the larger index one position to the right. 
                index_guide[j+1] = index_guide[j] #if key is less than swap
                j -= 1
            # Insert the key index into its correct position. 
            index_guide[j + 1] = key
        else:
            # Shift the indices to the right while the key's value is larger than the value in the sorted position.
            while j >= 0 and A.iat[i, col] > A.iat[index_guide[j], col]:
                # Shift the smaller index one position to the right.
                index_guide[j + 1] = index_guide[j]  # if key is less than swap
                j -= 1
            # Insert the key index into its correct descending order position. 
            index_guide[j + 1] = key
    # Reorder the entire DataFrame using the completed index guide.
    A.iloc[:] = A.iloc[index_guide].values


@timer_decorator
def insert_sort_rec(A, col, n=None, index_guide = None, asc=True):
    # Goal: Sorting DataFrame using recursive insert sort
    # A: DataFrame to sort
    # col: column position used for comparison
    # asc: should be True for ascending order, False for descending order

    # If n was not given, use the full length of the DataFrame.
    if n is None:
        n = len(A) # allows for dynamic sizing
    # If no index guide exists, create one that contains all row indices.
    if index_guide is None:
        index_guide = list(range(n))
    # Base Case: A prefix with 0 or 1 is already sorted.
    if n <= 1:
        return  index_guide
    
    # Start recursion by sorting the first n-1 rows. 
    # The same index guide is passed through every recursive call
    index_guide = insert_sort_rec(A, col, n = n - 1, index_guide = index_guide, asc= asc)

    # The last row in the sorted prefix is the key to insert. 
    key_index = index_guide[n-1]
    # Store the value of the key from the selected column. 
    key_val = A.iat[key_index,col]
    # Begin comparing the key with the row immediately before it.
    j = n - 2

    if asc == True:
        # Shift indices to the right while the key is smaller than the values in the sorted prefix.
        while j >= 0 and key_val < A.iat[index_guide[j], col]:
            # Move the larger index one position to the right.
            index_guide[j + 1] = index_guide[j]  # if key is less than swap
            j -= 1

    else:
        # Shift indices to the right while the key is larger than the values in the sorted prefix. 
        while j >= 0 and key_val > A.iat[index_guide[j], col]:
            # Move the smaller index position to the right.
            index_guide[j + 1] = index_guide[j]  # if key is less than swap
            j -= 1
    # Insert the key index into its correct position.
    index_guide[j + 1] = key_index

    # DataFrame is reordered after the entire recursive process finishes,
    if n == len(A):
        A[:] = A.iloc[index_guide].values
    # Return the index guide so every recursive call uses the same guide.
    return index_guide # So that it's using the same guide the entire time




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
    # Sort DataFrame using recursive selection sort.
    # i = first position in the unsorted portion of the DataFrame

    # Number of rows in the DataFrame
    length = A.iloc[:,col].size

    # If ascending is True, place the smallest value in the first unsorted position. 
    if asc == True:

        # Assume the first position in the unsorted portion contains the minimum value. 
        min = i

        # Search the remaining unsorted rows for a smaller value.
        for j in range(i + 1, length):

            # If a smaller index is found, store its row index. 
            if A.iat[j, col] < A.iat[min, col]:
                min = j
        # Swap the row at position i with the row containing the minimum value.
        A.iloc[[i, min]] = A.iloc[[min, i]].values
        
        # If more than one unsorted row remains, recursively sort the remaining portion of the DataFrame
        if i+1 < length:
            selection_sort_rec(A,col, asc = True, i = i+1)
    # If asc is False, sort the DataFrame in descending order by placing the largest value in the unsorted position.
    else:
        # Assume the first position in the unsorted portion contains the maximum value
        max = i

        # Search the remaining unsorted rows for a larger value.
        for j in range(i + 1, length):

            # If a larger value is found, store its row index.
            if A.iat[j, col] > A.iat[max, col]:
                max = j
        # Swap the row position at i with the row containing the maximum value.
        A.iloc[[i, max]] = A.iloc[[max, i]].values

        # If more than one unsorted row remains, recursively sort the remaining portion of the DataFrame. 
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
"""
def bin_search_iter(A,v):
  ###Return the index of v in sorted list A, or None if v is absent.
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
  ###Return the index of v in sorted list A, or None if v is absent.

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

    return search(0, len(A) - 1)"""

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

if __name__ == "__main__":
    print("<module name> : Is intended to be imported and not executed.")
