#  coding: utf-8
# ice1_analysis

from sort_and_search_funs import *
from util_funs import *
import pandas as pd

# This takes a sorted anndata_obj and filters
def filter_mt_cells(anndata_obj, mt_exp_lvl_threshold, gene_exp_threshold):
    if 0 > mt_exp_lvl_threshold or mt_exp_lvl_threshold >1:
        print("Mitochondrial expression threshold not valid.\
         Please use a number between 0 and 1.")
    elif 0 > gene_exp_threshold or gene_exp_threshold > 2000:
        print("Gene expression threshold not valid.\"
              "Please use a number between 0 and 2000.")
    else:
        print ("This is valid.") # Temporary

import anndata as ad
#Loads the .h5ad file into an AnnData object
#adata =  ad.read_h5ad("./data/pbmc_sample.h5ad")

# Note: the adata.T.var is a DF object.





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
