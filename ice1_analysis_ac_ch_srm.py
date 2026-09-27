#  coding: utf-8
# ice1_analysis

from sort_and_search_funs import *
from util_funs import *

import anndata as ad


def filter_mt_cells(anndata_obj, mt_exp_lvl_threshold, gene_exp_threshold):

    # ============================================================
    # 1. GET CELL DATAFRAME
    # ============================================================

    # Make a copy so original AnnData is not modified
    original_df = anndata_obj.T.var.copy()

    # Determine the column numbers for:
    # - mitochondrial expression %
    # - number of genes expressed
    #
    # TODO: fill these in after checking original_df.columns
    mt_col = ???
    gene_col = ???


    # ============================================================
    # 2. SORT BY MITOCHONDRIAL EXPRESSION -- DESCENDING
    # ============================================================

    # IMPORTANT:
    # Every sorting algorithm starts with a fresh copy of original_df

    # ---------- Iterative sorts ----------

    insert_iter_df = original_df.copy()
    insert_sort_iter(insert_iter_df, mt_col, asc=False)

    selection_iter_df = original_df.copy()
    selection_sort_iter(selection_iter_df, mt_col, asc=False)

    merge_iter_df = original_df.copy()
    merge_sort_iter(merge_iter_df, mt_col, asc=False)

    quick_iter_df = original_df.copy()
    quick_sort_iter(quick_iter_df, mt_col, asc=False)


    # ---------- Recursive sorts ----------

    insert_rec_df = original_df.copy()
    insert_sort_rec(insert_rec_df, mt_col, asc=False)

    selection_rec_df = original_df.copy()
    selection_sort_rec(selection_rec_df, mt_col, asc=False)

    merge_rec_df = original_df.copy()
    merge_sort_rec(merge_rec_df, mt_col, asc=False)

    quick_rec_df = original_df.copy()
    quick_sort_rec(quick_rec_df, mt_col, asc=False)


    # ============================================================
    # 3. SAVE MITOCHONDRIAL SORT TIMINGS
    # ============================================================

    # TODO:
    # Store timing results from each sorting algorithm.
    #
    # Exact implementation depends on how timer_decorator
    # returns/stores timing information.

    mt_sort_times = {
        # "Insertion Iterative": ...,
        # "Insertion Recursive": ...,
        # "Selection Iterative": ...,
        # etc.
    }


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


    # ============================================================
    # 6. SAVE GENE-EXPRESSION SORT TIMINGS
    # ============================================================

    gene_sort_times = {
        # "Insertion Iterative": ...,
        # "Insertion Recursive": ...,
        # etc.
    }


    # ============================================================
    # 7. FILTER LOW-GENE CELLS
    # ============================================================

    # Remove rows where number of genes expressed is LESS THAN
    # gene_exp_threshold.
    #
    # Repeat for each sorted DataFrame.


    # ============================================================
    # 8. RETURN RESULTS
    # ============================================================

    # We can decide exact return structure once timing functions
    # and all sorting functions are finished.

    # Possible structure:
    #
    # return {
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
    print(adata)
    print(adata.T.var.columns)
    print(adata.T.var.head())


    # ============================================================
    # RUN FILTER
    # ============================================================

    results = filter_mt_cells(
        adata,
        mt_exp_lvl_threshold=0.10,   # temporary test value
        gene_exp_threshold=200      # temporary test value
    )


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
