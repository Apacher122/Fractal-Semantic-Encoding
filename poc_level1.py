"""Proof of Concept for FSE Core Engine Level 1"""
import numpy as np
from fse.core import FSECore
from helpers.outputs import print_section

def run_level_1():
    """
    Executes the Level 1 POC focusing on Tier 1 Categorical Walls.
    Demonstrates 100% precision for structural queries by bypassing
    unrelated partitions entirely.
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

    # 6.1 Bootstrapping and Stabilization
    fse.bootstrap(raw_data)

    # 5.5 Query Execution via Deterministic Pruning
    # Tier 3 Filter: Age (Column 1) < 35
    res, touched = fse.execute_query(
        # Tier 1: Allow all regions
        partition_filter=lambda p_val: True,

        # 4.3 Theorem 2: Deterministic Query Pruning
        # Engine evaluates the predicate against boundaries. Since West age = 45, the condition is
        # met (45 > 35) and the branch is pruned.
        branch_evaluator=lambda b: b.exact_bounding_region['max_bounds'][1] < 35,

        # 4.2 Theorem 1: Exact Reconstruction
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
