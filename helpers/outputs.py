"""
This helper module contains output functions for the PoC and benchmarks.
"""

def print_section(section_title, is_subsection=False):
    """
    Outputs formatted section/sub-section headers.

    Args:
        section_title (str): Title of section/sub-section
        is_subsection (bool, optional): Indicates if this is a sub-section. Defaults to False.
    """
    divider = "-" if is_subsection else "="
    print("\n" + divider*90)
    print(section_title)
    print(divider*90)

def print_step(step_title, msg):
    """
    Outputs formatted step events.

    Args:
        step_title (str): Step title.
        msg (str): Information about the step.
    """
    print(f" [{step_title}] {msg}")

def print_benchmark_report(storage_metrics, query_results):
    """
    Calculates compression ratios and pruning efficiency, then outputs a 
    formatted ASCII table to the terminal.

    Args:
        storage_metrics (tuple): 3-element tuple containing the physical byte sizes of 
            (sqlite_size, parquet_size, fse_size).
        query_results (list of dict): A list of dictionaries containing the execution metrics for
                each query. Expected keys per dictionary:
            - 'name' (str): Query identifier.
            - 'baseline_rows' (int): Rows evaluated by baseline engines.
            - 'fse_rows' (int): Rows physically touched by FSE after pruning.
            - 'baseline_res' (float): Exact mathematical query result (via Pandas).
            - 'fse_res' (float): Approximate result calculated by FSE.
    """
    sql_size, pd_size, fse_size = storage_metrics

    # Calculate storage compression (in MB)
    sql_mb = sql_size / (1024 * 1024)
    pd_mb = pd_size / (1024 * 1024)
    fse_mb = fse_size / (1024 * 1024)

    # Calculate algorithmic efficiency
    comp_ratio = (1 - (fse_mb / sql_mb)) * 100

    print_section("BENCHMARK RESULTS")
    print_section("Storage Footprint", is_subsection=True)

    w = 30
    sql_text = f"{sql_mb:.2f} MB"
    pd_text = f"{pd_mb:.2f} MB"
    fse_text = f"{fse_mb:.2f} MB (-{comp_ratio:.1f}%)"
    print(
        f"{'SQLite (Raw B-Tree)':<{w}} | "
        f"{'Parquet (Snappy Columnar)':<{w}} | "
        f"{'FSE (Semantic Binary)':<{w}}"
    )
    print("-" * (w * 3 + 6))
    print(f"{sql_text:<{w}} | {pd_text:<{w}} | {fse_text:<{w}}")

    print_section("Query Workload Efficiency (rows scanned/touched)", is_subsection=True)
    print(
        f"{'Query Archetype':<38} |"
        f" {'Exact Result':<15} |"
        f" {'FSE Result':<12} |"
        f" {'Rows Touched (Pruning)'}"
    )

    for q in query_results:
        name = q['name']
        b_rows = q['baseline_rows']
        fse_rows = q['fse_rows']
        b_res = q['baseline_res']
        fse_res = q['fse_res']

        pruned = (1 - (fse_rows / b_rows)) * 100
        print(
            f"{name:<38} |"
            f" {b_res:<15.2f} |"
            f" {fse_res:<12.2f} |"
            f" {b_rows:,} vs {fse_rows:,} ({pruned:>5.1f}%)"
        )
    print("* Note: FSE Storage Footprint represents the actual byte size of the raw binary")
    print("  .fse file written to disk, demonstrating the physical reality of Delta Encoding.")
    print("  Parquet represents aggressive Snappy compression. SQLite represents raw disk storage.")
