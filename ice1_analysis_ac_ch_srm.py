#  coding: utf-8
# ice1_analysis

from sort_and_search_funs import *
from util_funs import *
import pandas as pd

import anndata as ad


def filter_mt_cells(anndata_obj, mt_exp_lvl_threshold, gene_exp_threshold, sorting_func):
    # Adding some things to just make it more useful overall, even though it's not exactly what is asked

    # ============================================================
    # 1. GET CELL DATAFRAME
    # ============================================================

    # Make a copy so original AnnData is not modified
    working_df = anndata_obj.T.var.copy(deep = True)

    mt_col = 2 # column for mitochondrial expression
    gene_col = 1 # column for genes expressed.

    timing_dict = {}
    func_name = sorting_func.__name__
    print(working_df.head(5))
    # ============================================================
    # 3. SAVE MITOCHONDRIAL SORT TIMINGS
    # ============================================================

    # TODO:
    # Store timing results from each sorting algorithm.
    #
    # Exact implementation depends on how timer_decorator
    # returns/stores timing information.
    # change this to add a regular timer block and manually input
    timing_dict[func_name] = {}
    timing_dict[func_name]["mt_sort_times"]= sorting_func(working_df, mt_col, asc = False)


    # ============================================================
    # 4. FILTER HIGH-MITOCHONDRIAL CELLS
    # ============================================================

    # Remove rows where mitochondrial expression is GREATER THAN
    # mt_exp_lvl_threshold.
    #
    # Do this for each sorted DataFrame.
    #
    # Example structure:
    #
    # insert_iter_filtered = ...
    # selection_iter_filtered = ...
    # etc.
    # using boolean indexing for now.
    mt_filtered_df = working_df[working_df.iloc[:,mt_col] > mt_exp_lvl_threshold]

    # ============================================================
    # 5. SORT REMAINING CELLS BY NUMBER OF GENES -- ASCENDING
    # ============================================================

    # Each algorithm now sorts its corresponding filtered
    # DataFrame using gene_col.
    #
    # Example:
    #
    # insert_sort_iter(insert_iter_filtered, gene_col, asc=True)
    #
    # Repeat for all iterative + recursive algorithms.
    timing_dict[func_name]["gene_sort_times"] = sorting_func(mt_filtered_df,
                                                                          gene_col, asc=True)

    # ============================================================
    # 6. SAVE GENE-EXPRESSION SORT TIMINGS
    # ============================================================


    # ============================================================
    # 7. FILTER LOW-GENE CELLS
    # ============================================================

    # Remove rows where number of genes expressed is LESS THAN
    # gene_exp_threshold.
    #
    # Repeat for each sorted DataFrame.
    gene_filtered_df = mt_filtered_df[mt_filtered_df.iloc[:,gene_col] < gene_exp_threshold]
    # ============================================================
    # 8. RETURN RESULTS
    # ============================================================

    # We can decide exact return structure once timing functions
    # and all sorting functions are finished.

    # Possible structure:
    #
    return gene_filtered_df, timing_dict
    #     "filtered_data": ...,
    #     "mt_sort_times": mt_sort_times,
    #     "gene_sort_times": gene_sort_times
    # }


def main():

    # ============================================================
    # LOAD scRNA-seq DATA
    # ============================================================

    adata = ad.read_h5ad("./data/pbmc_sample.h5ad")

    # Useful while developing
    #print(adata)
    #print(adata.T.var.columns)
    #print(adata.T.var.head())
    timing_dict = {}
    results_dict = {}
    # ============================================================
    # LIST OF SORTING METHODS TO USE
    # ============================================================
    #sorting_functions = [quick_sort_rec, selection_sort_iter,
     #                  selection_sort_rec, insert_sort_iter, insert_sort_rec]
    sorting_functions = [quick_sort_iter]
    # ============================================================
    # RUN FILTER
    # ============================================================
    for func in sorting_functions:

        results, timings = filter_mt_cells(adata,
                                       mt_exp_lvl_threshold=0.10, gene_exp_threshold=200,
                                       sorting_func = func)
        results_dict.update(results)
        timing_dict.update(timings)

    timings_df = pd.DataFrame.from_dict(timing_dict, orient = 'index')
    print(timings_df)


    #results = filter_mt_cells(
    #    adata,
    #    mt_exp_lvl_threshold=0.10,   # temporary test value
    #    gene_exp_threshold=200      # temporary test value
    #)


    # ============================================================
    # DISPLAY / SAVE RESULTS
    # ============================================================

    # TODO:
    # print timing table
    # save timing results
    # eventually create plots/table required for analysis


if __name__ == "__main__":
    main()

else:
    print("<module name> : Is intended to be executed and not imported.")
