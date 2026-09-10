#  coding: utf-8
# ice1_analysis

from sort_and_search_funs import *
from util_funs import *

import anndata as ad
#Loads the .h5ad file into an AnnData object
adata =  ad.read_h5ad("./data/pbmc_sample.h5ad")

def filter_mt_