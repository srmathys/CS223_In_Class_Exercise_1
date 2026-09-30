#  coding: utf-8
# ice1_analysis

from sort_and_search_funs import *
import pandas as pd
import plotly.express as px
import anndata as ad
import timeit
import sys


def filter_mt_cells(anndata_obj, mt_exp_lvl_threshold, gene_exp_threshold, sorting_func = "None"):
    # Adding some things to just make it more useful overall, even though it's not exactly what is asked

    # ============================================================
    # 1. GET CELL DATAFRAME
    # ============================================================

    # Make a copy so original AnnData is not modified
    working_df = anndata_obj.T.var.copy(deep = True)

    mt_col = 2 # column for mitochondrial expression
    gene_col = 1 # column for genes expressed.

    timing_dict = {}
    if sorting_func =="None":
        func_name = "None"
    else:
        func_name = sorting_func.__name__
    print ("\nRunning sorting function:", func_name)
    print("\nInitial Data frame with ", working_df.shape[0], "rows and ", working_df.shape[1], "columns")
    print(working_df.iloc[:5,:3])


    # ============================================================
    # 2. SORT BY MITOCHONDRIAL EXPRESSION -- DESCENDING
    # ============================================================
    # ============================================================
    # 3. SAVE MITOCHONDRIAL SORT TIMINGS
    # ============================================================
    # Sets up a timing dictionary with nested values for accessing later
    if func_name == "None":
        timing_dict[func_name] = {}
        timing_dict[func_name]["mt sort times"] = None
        working_df.sort_values(by=working_df.columns[mt_col],ascending=False,inplace=True)

    else:
        timing_dict[func_name] = {}
        timing_dict[func_name]["mt sort times"]= sorting_func(working_df, mt_col, asc = False)
    # no need to return a dataframe as the changes are reflected
    print("\nSorted by mitochondrial expression level")
    print("dataframe has size of", working_df.shape[0], "rows and ", working_df.shape[1], "columns")
    print(working_df.iloc[:5,:3])
    # ============================================================
    # 4. FILTER HIGH-MITOCHONDRIAL CELLS
    # ============================================================

    # Remove rows where mitochondrial expression is GREATER THAN
    # mt_exp_lvl_threshold.
    # assumes that there are no values under 0
    mt_filtered_df = working_df[working_df.iloc[:,mt_col] < mt_exp_lvl_threshold]
    print("\nfiltered by mitochondrial expression level threshold")
    print("New size is", mt_filtered_df.shape[0], "rows and ", mt_filtered_df.shape[1], "columns")
    print(mt_filtered_df.iloc[:5,:3])
    # ============================================================
    # 5. SORT REMAINING CELLS BY NUMBER OF GENES -- ASCENDING
    # ============================================================
    # ============================================================
    # 6. SAVE GENE-EXPRESSION SORT TIMINGS
    # ============================================================
    # Each algorithm now sorts its corresponding filtered
    # DataFrame using gene_col.

    if func_name == "None":
        timing_dict[func_name]["gene sort times"] = None
        mt_filtered_df.sort_values(by=mt_filtered_df.columns[gene_col],ascending=True,inplace=True)

    else:

        timing_dict[func_name]["gene sort times"] = sorting_func(mt_filtered_df,
                                                                          gene_col, asc=True)
    print("\nSorted by gene-expression levels")
    print("Dataframe has size of", mt_filtered_df.shape[0], "rows and ", mt_filtered_df.shape[1], "columns")
    print(mt_filtered_df.iloc[:5,:3])



    # ============================================================
    # 7. FILTER LOW-GENE CELLS
    # ============================================================

    # Remove rows where number of genes expressed is LESS THAN
    # gene_exp_threshold.
    #
    # Repeat for each sorted DataFrame.
    gene_filtered_df = mt_filtered_df[mt_filtered_df.iloc[:,gene_col] > gene_exp_threshold]
    # Save final to a dictionary to pass out for further storage
    results_dict = {}
    results_dict[func_name] = gene_filtered_df


    print("Filtered by gene-expression level threshold")
    print("Final size is", gene_filtered_df.shape[0], "rows and ", gene_filtered_df.shape[1], "columns")
    print(gene_filtered_df.iloc[:5,:3])
    # ============================================================
    # 8. RETURN RESULTS
    # ============================================================

    # We can decide exact return structure once timing functions
    # and all sorting functions are finished.

    # Possible structure:
    #
    return results_dict, timing_dict
    #     "filtered_data": ...,
    #     "mt_sort_times": mt_sort_times,
    #     "gene_sort_times": gene_sort_times
    # }


def main():

    # ============================================================
    # LOAD scRNA-seq DATA
    # ============================================================

    adata = ad.read_h5ad("./data/pbmc_sample.h5ad")

    # Setting up dictionaries in order to store results and timing information

    timing_dict = {}
    results_dict = {}
    # ============================================================
    # LIST OF SORTING METHODS TO USE
    # ============================================================
    sorting_functions = [insert_sort_iter, insert_sort_rec, selection_sort_iter, selection_sort_rec,
                         merge_sort_iter, merge_sort_rec, quick_sort_iter, quick_sort_rec]

    #sorting_functions = [insert_sort_rec, selection_sort_rec,quick_sort_rec,merge_sort_rec,]
    #
    ## Some of the recursion functions like insert_sort recursive have large stack overheads
    ## Increasing the stack size in order to not max out recursion limit

    sys.setrecursionlimit(2000)

    # ============================================================
    # RUN FILTER
    # ============================================================
    for func in sorting_functions:

        results, timings = filter_mt_cells(adata,
                                       mt_exp_lvl_threshold=0.10, gene_exp_threshold=200,
                                       sorting_func = func)
        results_dict.update(results)
        timing_dict.update(timings)


    # ============================================================
    # DISPLAY / SAVE RESULTS
    # ============================================================

    #Import Timing dictionary (timing_dict) to Dataframe Object from Dictionary
    # Make every column with a header. Sort lowest to highest based on first step
    # Print the timings dataframe and export dataframe as tsv for later use in output folder
    # Export dataframe as tsv for later

    timings_df = pd.DataFrame.from_dict(timing_dict, orient = 'index')
    timings_df.index.name = "sorting function"
    timings_df.sort_values(by= timings_df.columns[0], ascending = True, inplace = True)
    timings_df.to_csv("./output/timings.tsv",sep = '\t', index = True)
    print(timings_df)


    #Create a tidy dataframe for plotting
    # Using an interactive graph with plotly for easily visualization
    # This requires melting the dataframe in a long form
    tidy_df = pd.melt(timings_df.reset_index(),
        id_vars = "sorting function",
        value_vars = ['mt sort times', 'gene sort times'],
        var_name = "sorting step",
        value_name = "time"
    )


    fig = px.bar(
        tidy_df,
        x = "sorting step",
        y = "time",
        color = "sorting function",
        barmode = "group",
        title = "Sorting Function Efficiency by Task",
        labels={"sorting step":"Sorting Step", "time":"Time (s)", "sorting function":"Sorting Function"},
        text_auto = '.2e'
    )
    fig.update_traces(textposition='outside')
    fig.show()
    fig.write_html("./output/timings_graph.html")

if __name__ == "__main__":
    main()

else:
    print("<module name> : Is intended to be executed and not imported.")
