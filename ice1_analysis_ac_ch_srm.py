#  coding: utf-8
# ice1_analysis

from sort_and_search_funs import *
from util_funs import *

import anndata as ad
#Loads the .h5ad file into an AnnData object
adata =  ad.read_h5ad("./data/pbmc_sample.h5ad")

def filter_mt_cells(anndata_obj, mt_exp_lvl_theshold, gene_exp_threshold):






if __name__ == "__main__": 
  main()
else:
  print("<module name> : Is intended to be executed and not imported.")
