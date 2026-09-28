#  coding: utf-8
# Sort and search functions
import pandas as pd


from util_funs import timer_decorator


# note: A.iat gets a single value using integer positioning in pandas
@ timer_decorator
def insert_sort_iter(A,col,asc = True): #A is a dataframe, col is number
    size = A.iloc[:,col].size
    if size <= 1:
        return

    index_guide = list(range(size))
    # Shifting values in a premade list in order to track where insertions are happening

    for i in range(1,size):
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
    A.iloc[list(range(size))] = A.iloc[index_guide].values


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
  
@ timer_decorator
def insert_sort_rec(A: pd.DataFrame,col,n = None,asc = True):
    if n is None:
      n = A.iloc[:,col].size #allows for dynamic sizing
    if n <= 1:
        return # done with recursing
    #start recursions
    insert_sort_rec(A,col,n-1, asc)

    key_row = A.iloc[n-1].copy()
    key_val = key_row.iloc[col]

    j = n - 2
    if asc == True:
        while j >= 0 and key_val < A.iat[j, col]:
            A.iloc[j + 1] = A.iloc[j]  # if key is less than swap
            j -= 1

        A.loc[j + 1] = key_row
    else:
        while j >= 0 and key_val > A.iat[j, col]:
            A.iloc[j + 1] = A.iloc[j]  # if key is less than swap
            j -= 1

        A.loc[j + 1] = key_row




@timer_decorator
def selection_sort_iter(A,col = 0,asc = True):
    length = A.iloc[:,col].size
    if asc == True:
        for i in range(length -1):
            # finding the minimum element in the unsorted sublist from a dataframe column
            # once found, it can be swapped with the index of i
            min = i
            for j in range(i+1,length):
                if A.iat[j,col] < A.iat[min,col]:
                    min = j
            A.iloc[[i,min]] = A.iloc[[min,i]].values
    else:
        for i in range(length - 1): #same thing, but with max
            max = i
            for j in range(i+1,length):
                if A.iat[j,col] > A.iat[max,col]:
                    max = j
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



if __name__ == "__main__":
    print("<module name> : Is intended to be imported and not executed.")
