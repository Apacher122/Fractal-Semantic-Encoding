"""
Proof of Concept for FSE Core Engine Level 2
Demonstrates Tier 1 Isolation and Tier 2 Autonomous Bifurcation via Saturation Limits."""
import numpy as np
from fse.core import FSECore, SemanticPattern
from helpers.outputs import print_section

# 7.1 Out-of-Bounds Detection
THRESHOLD_TOLERANCE_TAU = 2.5 # scalar limit for Mahalanobis distance

# 7.3 Autonomous Bifurcation
SATURATION_THRESHOLD_THETA = 1 # critical cardinality limit of the Elastic Buffer

def calculate_mahalanobis_mock(record, centroid):
    """
    Micro-datasets with zero-variance categorical columns will lead to a singular matrix problem if
    calculating the Mahalanobis distance. For this proof of concept, the mock function simply
    returns the Euclidean distance.
    """
    return np.linalg.norm(record - centroid)

def run_level_2():
    """
    Validates the FSE engine's ability to handle data drift and new categorical discovery while
    maintaining 100% EQP integrity.
    """
    print_section("FSE MICRO PoC - LEVEL 2: ADAPTIVE MANIFOLD (TIERS 2 & 3)")

    # Using the same dataset as Level 1
    raw_data = np.array([
        [1, 31, 120], [1, 34, 115], [1, 33, 200], [1, 32, 195], # East
        [2, 45, 130], [2, 47, 210], [2, 46, 125], [2, 46, 205], # West
        [3, 28,  90], [3, 27, 150], [3, 29,  95], [3, 28, 155]  # North
    ])

    print_section("Bootstrapping FSE Database", is_subsection=True)
    db = FSECore(partition_col=0, n_sub_clusters=2)
    db.bootstrap(raw_data)

    print(f"System Baseline Established: {len(db.partitions)} Deterministic Partitions (Tier 1)")
    print(f"Fractal Saturation Limit set to: {SATURATION_THRESHOLD_THETA}")

    # Chapter 7: Adaptive Evolution
    streaming_data = np.array([
        [1, 32, 125], # Normal East buyer (Should assimilate normally)
        [4, 40, 300], # South buyer 1 (Extreme anomaly)
        [4, 42, 310]  # South buyer 2 (Extreme anomaly)
    ])

    print_section("Ingesting Streaming Data", is_subsection=True)
    global_elastic_buffer = []

    for record in streaming_data:
        p_val = record[0]

        if p_val in db.partitions:
            print(
                f"Record {record}: Categorical Match found (Tier 1: Partition {p_val}). "
                "Assimilating as Delta."
            )

            pattern = db.partitions[p_val][0]

            # 7.1 Out-of-Bounds Detection
            m_dist = calculate_mahalanobis_mock(record, pattern.semantic_centroid)

            if m_dist > THRESHOLD_TOLERANCE_TAU:
                print(
                    f"Record Distance: {m_dist:.2f} (Tolerance: {THRESHOLD_TOLERANCE_TAU:.2f}). ")

                # 7.2 The Eleastic Buffer
                print(" -> Routing anomalous record to Elastic Buffer.")
                pattern.elastic_buffer.append(record)
            else:
                # 5.4 Tier 3: Residual Encoding
                print("Assimilating record as Delta.")
        else:
            print(f"Record {record}: No categorical match. Triggering Autonomous Bifurcation...")
            print(" -> Record violates existing structural manifold.")

            # 7.2 The Eleastic Buffer
            print(" -> Routing anamalous record to Elastic Buffer.")
            global_elastic_buffer.append(record)

            # 7.3 Autonomous Bifurcation
            if len(global_elastic_buffer) > SATURATION_THRESHOLD_THETA:
                print(" -> Elastic Buffer saturation threshold reached.")
                print(" -> Triggering Fractal Saturation.")
                print(" -> Triggering Tier 2 Autonomous Bifurcation.")

                # Instantiate emergent prototype
                new_pattern = SemanticPattern(partition_key=p_val)
                new_pattern.semantic_centroid = record
                new_pattern.exact_bounding_region = {
                    'min_bounds': record,
                    'max_bounds': record
                }
                new_pattern.delta_vectors = [np.array([0, 0, 0])]
                db.partitions[p_val] = [new_pattern]

                # clear buffer
                global_elastic_buffer.clear()


    # final system state
    print_section("Final System State", is_subsection=True)
    print(f"Total Tier 1 Partitions: {len(db.partitions)}")

    latest_region = 4
    latest_branch = db.partitions[latest_region][0]

    print(f"New Emergent Prototype (Region {latest_region}):")
    print(f" -> Centroid: {latest_branch.semantic_centroid}")
    print(f" -> Exact Bounding Matrix Floor (Min): {latest_branch.exact_bounding_region['min_bounds']}")
    print(f" -> Exact Bounding Matrix Ceiling (Max): {latest_branch.exact_bounding_region['max_bounds']}")
    print("-" * 60)


if __name__ == "__main__":
    run_level_2()
