#  coding: utf-8
# ice1_analysis

from sort_and_search_funs import *
from util_funs import timer_decorator
import pandas as pd
import anndata as ad
#Loads the .h5ad file into an AnnData object
#adata =  ad.read_h5ad("./data/pbmc_sample.h5ad")

#def filter_mt_

# testing the sort
execution_log = {}

data = {
    'Gene' : ['CTCF','HTT','DND','KCQN1'],
    'Section': [19,12,8,11],
    'Average':[8.7,8,7.5,9]
}
df = pd.DataFrame(data)

print(quick_sort_rec(df,1,asc = False))
print(df)
