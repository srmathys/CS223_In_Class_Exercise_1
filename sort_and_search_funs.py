#  coding: utf-8
# Sort and search functions
import pandas as pd

from util_funs import timer_decorator


# note: A.iat gets a single value using integer positioning in pandas
@ timer_decorator
def insert_sort_iter(A,col = 0,asc = True): #A is a dataframe, col is number
    for i in range(1,A.iloc[:,col].size):
        key = A.iat[i,col]
        j = i - 1
    if asc == True:
        while j >= 0 and key < A.iat[j,col]:
            A.iloc[[j+1,j]] = A.loc[[j,j+1]].values #if key is less than swap
            j -= 1
    else:
        while j >= 0 and key > A.iat[j,col]:
            A.iloc[[j+1,j]] = A.loc[[j,j+1]].values
            j -= 1
# limitations: I don't know how to shift in pandas the way it would be done in a list

@ timer_decorator
def insert_sort_rec(A: pd.DataFrame,col: int,n = None,asc = True):
    if n is None:
      n = A.iloc[:,col].size #allows for dynamic sizing
    if n < 1:
        return # done with recursing
    #start recursions
    insert_sort_rec(A,col,n-1, asc)
    key = A.iat[n-1, col]
    j = n - 2
    if asc == True: #setting the movements
        while j >= 0 and key < A.iat[j,col]:
            A.iloc[[j+1,j]] = A.iloc[[j,j+1]].values # if key is less than swap
            j -= 1
    else:
        while j >= 0 and key > A.iat[j,col]:
            A.iloc[[j+1,j]] = A.iloc[[j,j+1]].values
            j-= 1




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


#@ timer_decorator
#def merge_sort_iter(A: pd.DataFrame,col: int,asc = True):


#@ timer_decorator
#def merge_sort_rec(A: pd.DataFrame,col: int,asc = True):


#@ timer_decorator
#def quick_sort_iter(A: pd.DataFrame,col: int,asc = True):
#
#
#
#
#


@ timer_decorator
def quick_sort_rec(A,col,low = 0, high = None ,asc = True):
#Recursively sorting using quicksort
    if high is None:
        high = A.iloc[:,col].size -1
    if low < high:
        #integrate lomuto partitioning
        pivot_val = A.iat[high,col] #value of the last element for pivot
        i = low
        if asc == True: #allows for both types of sorting
            for j in range(low, high):
                if A.iat[j,col]<= pivot_val:
                    A.iloc[[j,i]] = A.iloc[[i,j]].values
                    i += 1
        else:
            for j in range(low, high):
                if A.iat[j,col]>= pivot_val:
                    A.iloc[[j,i]] = A.iloc[[i,j]].values
                    i += 1
        A.iloc[[high,i]] = A.iloc[[i,high]].values

        quick_sort_rec(A,col,low,i-1,asc)
        quick_sort_rec(A,col, i+1,high,asc)

#@ timer_decorator
#def bin_search_iter(A: pd.DataFrame,col: int,asc = True):


#@ timer_decorator
#def bin_search_rec(A: pd.DataFrame,col: int,asc = True):

if __name__ == "__main__":
    print("<module name> : Is intended to be imported and not executed.")