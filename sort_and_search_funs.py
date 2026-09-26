#  coding: utf-8
# Sort and search functions
import pandas as pd
# note: A.iat gets a single value using integer positioning in pandas

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

#def insert_sort_rec(A: pd.DataFrame,col: int,asc = True):

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

#def merge_sort_iter(A: pd.DataFrame,col: int,asc = True):

#def merge_sort_rec(A: pd.DataFrame,col: int,asc = True):

#def quick_sort_iter(A: pd.DataFrame,col: int,asc = True):

#def quick_sort_rec(A: pd.DataFrame,col: int,asc = True):

#def bin_search_iter(A: pd.DataFrame,col: int,asc = True):

#def bin_search_rec(A: pd.DataFrame,col: int,asc = True):

if __name__ == "__main__":
    print("<module name> : Is intended to be imported and not executed.")