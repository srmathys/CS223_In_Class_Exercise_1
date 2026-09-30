#  coding: utf-8
# Sort and search functions
import pandas as pd
import numpy as np
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
    # using a value list for easy checking
    vals = A.iloc[:,col].to_numpy()
    # Shifting values in a premade list in order to track where insertions are happening

    # Begin at the second row because the first row is already sorted.
    for i in range(1,n):
        # Compare the current row with the row before it. 
        j = i - 1
        # Store the index of the row being inserted.
        key = index_guide[i]
        # Using the index_guide
        if asc == True:
            # Shift the indices to the right while the value of the key is smaller than the value in the sorted portion.
            while j >= 0 and vals[i] < vals[index_guide[j]]:
      # Shift the larger index one position to the right. 
                index_guide[j+1] = index_guide[j] #if key is less than swap
                j -= 1
            # Insert the key index into its correct position. 
            index_guide[j + 1] = key
        else:
          # Shift the indices to the right while the key's value is larger than the value in the sorted position.
            while j >= 0 and vals[i] > vals[index_guide[j]]:
     # Shift the smaller index one position to the right.
                index_guide[j + 1] = index_guide[j]  # if key is less than swap
                j -= 1
            # Insert the key index into its correct descending order position. 
            index_guide[j + 1] = key
    # Reorder the entire dataframe using the completed index guide
    A.iloc[:] = A.iloc[index_guide].values


@timer_decorator
def insert_sort_rec(A, col, n=None, index_guide = None, asc=True):
    # Goal: Sorting DataFrame using recursive insert sort
    # A: DataFrame to sort
    # col: column position used for comparison
    # asc: should be True for ascending order, False for descending order

    # pulling out a list of values for quick checking
    vals = A.iloc[:,col].to_numpy()
    # If n was not given, use the full length of the DataFrame.
    if n is None:
        n = len(A) # allows for dynamic sizing
    # If no index guide exists, create one that contains all row indices.
    if index_guide is None:
    # creating a guide list to help with reordering at the end
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
    key_val = vals[key_index]
  # Begin comparing the key with the row immediately before it.
    j = n - 2

    if asc == True:
      # Shift indices to the right while the key is smaller than the values in the sorted prefix.
        while j >= 0 and key_val < vals[index_guide[j]]:
           # Move the larger index one position to the right.
            index_guide[j + 1] = index_guide[j]  # if key is less than swap
            j -= 1

    else:
      # Shift indices to the right while the key is larger than the values in the sorted prefix. 
        while j >= 0 and key_val > vals[index_guide[j]]:
        # Move the smaller index position to the right.
            index_guide[j + 1] = index_guide[j]  # if key is less than swap
            j -= 1
    # Insert the key index into its correct position.
    index_guide[j + 1] = key_index

    # DataFrame is reordered after the entire recursive process finishes,
    if n == len(A):
        A[:] = A.iloc[index_guide].values
        return
  # Return the index guide so every recursive call uses the same guide if not on original stack
    return index_guide # So that it's using the same guide for the entire time


@timer_decorator
def selection_sort_iter(A,col = 0,asc = True):
 
    # Goal: Sorting a DataFrame using iterative selection sort.
    # A: DataFrame to sort
    # col: column position used for comparison
    # asc: should be True for ascending order, False for descending order

    # Obtain the number of rows in the DataFrame
    # Use them to create a guidance list for tracking index swaps
    # Then pull values into a separate array for ease of lookups
    length = len(A)
    index = list(range(length))
    vals = A.iloc[:,col].to_numpy()

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
                if vals[index[j]] < vals[index[min]]:
                    min = j
            # Exchange the selected minimum row with row i
            # Entire row is exchanged, not just the selected column
            index[i],index[min] = index[min], index[i]
    else:
        # Descending-order version searches for the maximum. Otherwise same as above
        for i in range(length - 1): #same thing, but with max
            # Assume the first element in the unsorted portion is the largest element.
            max = i

            # Search the remaining unsorted portion of the column.
            for j in range(i+1,length):

                # Update the max if a larger value is found. 
                if vals[index[j]] > vals[index[max]]:
                    max = j
            index[i],index[max] = index[max], index[i]

    # When done use the index guide that was made to place all values in the correct order
    A.iloc[:] = A.iloc[index].values

@ timer_decorator
def selection_sort_rec(A,col = 0,asc = True, index = None,  i = None):
    # Goal: Sorting a DataFrame using recursive selection sort.
    # A: DataFrame to sort
    # col: column position used for comparison
    # asc: should be True for ascending order, False for descending order
    # index tracks an index guide around, i is the iteration point

    # Obtain the number of rows in the DataFrame
    length = len(A)
    #Create list of values to compare
    vals = A.iloc[:,col].to_numpy()
    if i is None:
        # setting up the index for the first one in the stack
        index = list(range(length))
        i = 0
    else:
        # pass through premade index guide on later loops
        index = index

    if asc == True:
        # finding the minimum element in the unsorted sublist from a dataframe column
        # once found, it can be swapped with the index of i
        # Assume that the first element in the unsorted portion is the smallest element.
        min = i

        for j in range(i + 1, length):
            # Update the min if a smaller value is found.
            if vals[index[j]] < vals[index[min]]:
                min = j
        # Exchange the selected minimum row with row i
        # Entire row is exchanged, not just the selected column
        index[i],index[min] = index[min], index[i]

        if i+1 < length:
        # if not all checked then just recurse through to make more stacks
            index = selection_sort_rec(A,col, asc = asc, index= index, i = i+1)

    # Used for descending sort, same as above but with max instead of min.
    else:
        # Assume the first position in the unsorted portion contains the maximum value
        max = i

        # Search the remaining unsorted rows for a larger value.
        for j in range(i + 1, length):
          # If a larger value is found, store its row index.
            if vals[index[j]] > vals[index[max]]:
                max = j
      # Swap the index row position at i with the row containing the maximum value.
        index[i],index[max] = index[max], index[i]
      # If more than one unsorted row remains, recursively sort the remaining portion of the DataFrame. 

        if i+1 < length:
            index = selection_sort_rec(A,col, asc = asc, index = index, i =i+1)
    if i > 0:
        #allows for later loops to give returns and pass the index guide down
        return index
    # On final loop triggers this as i will be equal to 0
    A.iloc[:] = A.iloc[index].values

### Helper functions for Quicksort ###
## Using the median of three pivoting  ##
def median_of_three(vals, index, low, high, asc):
    # Using Median of Three Pivot position
    # Locations of low and high used to go through index_guide
    # index guide used to call correct values from the dataframe to compare
    # pass index guide through in order to save the changes


    mid = low + (high - low) // 2
    # sorting the low, mid and high positions in place
    # One version if ascending order, one if not
    # the swapping is done on the index guide, not on the real dataframe
    if asc == True:
        if vals[index[high]] < vals[index[low]]:
            index[low],index[high] = index[high], index[low]
        if vals[index[mid]] < vals[index[low]]:
            index[low],index[mid] = index[mid], index[low]
        if vals[index[high]] < vals[index[mid]]:
            index[mid],index[high] = index[high], index[mid]

    # descending version
    else:
        if vals[index[high]] > vals[index[low]]:
            index[low],index[high] = index[high], index[low]
        if vals[index[mid]] > vals[index[low]]:
            index[low],index[mid] = index[mid], index[low]
        if vals[index[high]] > vals[index[mid]]:
            index[mid],index[high] = index[high], index[mid]
     # swaps mid and high to make new pivot value for partitions
    index[mid], index[high] = index[high], index[mid]
    return vals[index[high]], index

## Helper for Quicksort on working with partitioning ##
def partition(vals, index, low, high, asc):

    # Use the pivot value helper function
    # Take the dataframe ref, column, index_guide and low and high slice locations
    # Use the dataframe to get the values of interest

    pivot_val, index = median_of_three(vals, index, low, high, asc)
    i = low - 1
    if asc == True:
        for j in range(low, high):
            if vals[index[j]] <= pivot_val:
                i += 1
                index[i], index[j] = index[j], index[i]
    else:
        for j in range(low, high):
            if vals[index[j]] >= pivot_val:
                i += 1
                index[i], index[j] = index[j], index[i]
    index[i + 1], index[high] = index[high], index[i + 1]
    return i + 1, index

@ timer_decorator
def quick_sort_iter(A ,col, asc = True):

    #Iterative sorting using quicksort
    #Takes a dataframe, column of interest to sort, and whether it is ascending or not

    vals = A.iloc[:,col].to_numpy()
    index = list(range(len(A)))
    #### Creating initial stack size
    # This stack is a list with a tuple
    stack = [(0, len(A) - 1)]

    ### pushing initial values into the stack
    # as long as there are items in the stack run this loop
    while stack:
    # When you pop from a list, it returns the tuple
    # we assign each element of the tuple to an index value
        low, high = stack.pop()
        if low < high:
            #
            p , index = partition(vals, index, low, high, asc)
    # Try to grab the larger size of the partition to deal with first
            left_side_size = p - low
            right_side_size = high - p

            if left_side_size > right_side_size:
    # This means left is the bigger side of the partition
        # Add tuples for slices to go through, first left then right
                stack.append((low, p-1))
                stack.append((p+1, high))
            else:
    # This means right side is bigger or they are the same size
        # Add tuples for slices, first right then left
                stack.append((p + 1, high))
                stack.append((low, p-1))
    # do the final swapping
    A.iloc[:] = A.iloc[index].values

@ timer_decorator
def quick_sort_rec(A,col, index = None, low = 0, high = None ,asc = True):
    top_level = index is None
    vals = A.iloc[:,col].to_numpy()
    if high is None:
        high = len(A) - 1
    if index is None:
        top_level = True
        index = list(range(len(A)))
    if low < high:
        pivot_loc,index = partition(vals, index, low, high, asc)

        quick_sort_rec(A,col,index, low, pivot_loc-1, asc)
        quick_sort_rec(A,col,index, pivot_loc+1, high, asc)
    if top_level:
        A.iloc[:] = A.iloc[index].values
    else:
        return index

# Merge Sort Helper Function

def merge(vals, index, left: int, middle: int, right: int, asc=True):
    # Merge helper function
    # takes the vals from the array column (list)
    # values of slicing indexes (left, middle right)
    # sorting method (ascending or descending)

    # creates two different subarrays
    # remember array slices are up to on the right
    left_array = index[left:middle + 1]
    right_array = index[middle + 1: right+1]

    # setting indices. Making k based on beginning of slice to iterate properly
    i = j = 0
    k = left

    # go through the two sides of the array
    # Make a comparison with the first values from each array based on the final sort
    # (ascending/descending)
    # iterate k

    while i < len(left_array) and j < len(right_array):
        val_left = vals[left_array[i]]
        val_right = vals[right_array[j]]

        # Handle ascending vs descending comparison
        condition = (val_left <= val_right) if asc else (val_left >= val_right)
        # ascending puts values on on the left. descending on the right
        # tied values go on the left

        if condition:
            index[k] = left_array[i]
            i += 1
        else:
            index[k] = right_array[j]
            j += 1
        k += 1
    # add the remaining things to the right
    remaining = left_array[i:] or right_array[j:]
    index[k:k + len(remaining)]= remaining
    return index

@ timer_decorator
def merge_sort_iter(A: pd.DataFrame, col: int, asc=True):
    n = len(A)
    vals = A.iloc[:,col].to_numpy()
    index = list(range(len(A)))
    curr_size = 1

    while curr_size < n:
        left_start = 0
        while left_start < n - 1:
            mid = min(left_start + curr_size - 1, n - 1)
            right_end = min(left_start + 2 * curr_size - 1, n - 1)

            # Pass col and asc down to the merge function
            index = merge(vals, index, left_start, mid, right_end, asc)
            left_start += 2 * curr_size

        curr_size *= 2
    # Final Swapping
    A.iloc[:] = A.iloc[index].values

@ timer_decorator
def merge_sort_rec(A: pd.DataFrame, col: int, asc: bool = True, index = None, vals = None, left = 0, right = None):
    # setting an indicator when it hits the bottom of the stack
    top_level = index is None

    #setting up helper values
    if top_level:
        # checks to make sure it's even worth sorting
        if len(A) <= 1:
            return
        # sets up the helper lists for speed
        vals = A.iloc[:,col].to_numpy()
        index = list(range(len(A)))
        # initializing right to the last index
        right= len(A) -1
    # goes through the different sides
    if left < right:
        mid = left + (right - left)//2
        index = merge_sort_rec(A, col, asc, index, vals, left, mid)
        index = merge_sort_rec(A,col,asc,index, vals, mid + 1, right)
        index = merge(vals, index, left, mid, right, asc)
    # when it gets back to first part of stack
    if top_level:
        A.iloc[:] = A.iloc[index].values
    # returns the index it's been mutating
    else:
        return index

### Search Algorithms ###

def bin_search_iter(A, col, value, asc = True, exact = True):
  
  ###Return the index of v in sorted list A, or -1 if v is absent."""
    low = 0
    high = len(A) - 1
    result_idx = -1 # set it to not found to start
    
  ## These are index values, allows us to be more specific here
    if asc == True:
        while low <= high:
            mid = (low + high) // 2

            if A.iat[mid,col] <= value:
                result_idx = mid
                low = mid + 1
            else:
                high = mid - 1
    else:
        while low <= high:
            mid = (low + high) // 2

            if A.iat[mid, col] >= value:

                low = mid + 1
            else:
                result_idx = mid
                high = mid - 1
    return result_idx



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
