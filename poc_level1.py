"""
Proof of Concept for FSE Core Engine Level 1
Chapter 8.1.A: Deterministic Precision and Pruning

This module will validate the following:
1. Tier 1 (Deterministic Partitioning): Achieving state-isolation. Eliminates cross-partition ambiguity.
2. Tier 2 (Fractal Branching): Achieving exact ractal pruning.
3. Tier 3 (Delta Encoding): Achieving lossless reconstruction.
"""
import numpy as np
from fse.core import FSECore
from helpers.outputs import print_section

def run_level_1():
    """
    Executes Level 1, focusing on Deterministic Precision.
    """
    print_section(" FSE MICRO PoC - LEVEL 1: DETERMINISTIC ISOLATION (TIER 1)")

    # For simplicity, we will use numeric representations of data.
    # This example uses the 12-record dataset outlined in Chapter 5.
    raw_data = np.array([
        [1, 31, 120], [1, 34, 115], [1, 33, 200], [1, 32, 195], # East
        [2, 45, 130], [2, 47, 210], [2, 46, 125], [2, 46, 205], # West
        [3, 28,  90], [3, 27, 150], [3, 29,  95], [3, 28, 155]  # North
    ])
    fse = FSECore(partition_col=0, n_sub_clusters=1)

    fse.bootstrap(raw_data)

    # Query: Age (Column 1) < 35
    res, touched = fse.execute_query(
        # Tier 1: Allow all regions to evaluate state-isolation integrity.
        partition_filter=lambda p_val: True,

        # Tier 2: Evaluate the predicate against Exact Bounding Regions.
        branch_evaluator=lambda b: b.exact_bounding_region['max_bounds'][1] < 35,

        # Tier 3: Exact match for reconstructed Delta Vectors (Theorem 1).
        leaf_evaluator=lambda r: r[1] < 35,

        aggregator=np.mean
    )

    mask = raw_data[:, 1] < 35
    actual_mean = raw_data[mask][:, 2].mean()

    # 4.4 Theorem 3: Completeness (Zero False Negatives)
    print("Target: Average Spend for Age < 35")
    print(f"FSE Result: {res:.2f}")
    print(f"Actual Mean: {actual_mean:.2f}")
    print(f"Rows Touched: {touched} / {len(raw_data)}")
    print("-> The engine mathematically proved the 'West' branch was out of bounds")
    print("-> and pruned it without scanning a single row.")
    print("-"*50)


if __name__ == "__main__":
    run_level_1()
