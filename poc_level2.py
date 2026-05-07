"""
Proof of Concept for FSE Core Engine Level 2
Chapter 8.1.B: Adaptive Evolution and Autonomous Bifurcation

This module will validate the following:
1. Out-of-Bounds Detection: Detecting data drift and new categorical discovery.
2. The Elastic Buffer: Routing anomalous to transient storage to preserve pruning efficiency.
3. Autonomous Bifurcation: Dynamic instantiation of a new mathematical centroid once saturation
    threshold is exceeded.
"""
import numpy as np
from fse.core import FSECore, SemanticPattern
from helpers.outputs import print_section
from scipy.spatial.distance import mahalanobis

# Scalar limit for Mahalanobis distance
THRESHOLD_TOLERANCE_TAU = 2.5 

# Critical cardinality limit that triggers Autonomous Bifurcation
SATURATION_THRESHOLD_THETA = 1

def calculate_mahalanobis_distance(record, cluster_data, centroid):
    """
    Calculates the Mahalanobis distance between a record and the centroid of a cluster.
    """
    if len(cluster_data) <= 1:
        return np.linalg.norm(record - centroid)

    # 1. Calculate covariance
    cov = np.cov(cluster_data, rowvar=False)
    
    # 2. Moore-Penrose Psuedo-Inverse to prevent Singular Matrix crashes
    cov_inv = np.linalg.pinv(cov)

    # 3. Calculate Mahalanobis distance
    return mahalanobis(record, centroid, cov_inv)

def run_level_2():
    """
    Executes Level 2, validating Adaptive Evolution.
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

    # Drift simulation w/ extreme statistical anomalies
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
            print(f"Record {record}: Categorical Match found (Tier 1: Partition {p_val}).")

            pattern = db.partitions[p_val][0]

            cluster_data = [pattern.semantic_centroid + delta for delta in pattern.delta_vectors]

            # Step 1: Out-of-Bounds Detection
            m_dist = calculate_mahalanobis_distance(record, cluster_data, pattern.semantic_centroid)

            if m_dist > THRESHOLD_TOLERANCE_TAU:
                print(
                    f"Record Distance: {m_dist:.2f} (Tolerance: {THRESHOLD_TOLERANCE_TAU:.2f}). ")

                # Step 2: The Eleastic Buffer
                print(" -> Routing anomalous record to Elastic Buffer.")
                pattern.elastic_buffer.append(record)
            else:
                print("Assimilating record as Delta Vector.")
        else:
            print(f"Record {record}: Unmmaped Category (Tier 1: Partition {p_val}).")
            print(" -> Record violates existing structural manifold.")

            min_distance = float('inf')
            closest_region = None

            for known_p_val, patterns in db.partitions.items():
                pattern = patterns[0]
                cluster_data = [pattern.semantic_centroid + delta for delta in pattern.delta_vectors]
                m_dist = calculate_mahalanobis_distance(record, cluster_data, pattern.semantic_centroid)

                if m_dist < min_distance:
                    min_distance = m_dist
                    closest_region = known_p_val
            
            print(f" -> Evaluated against closest region: {closest_region}.")

            # Step 1: Out-of-Bounds Detection
            if min_distance > THRESHOLD_TOLERANCE_TAU:
                print(f" -> Record Distance: {min_distance:.2f} (Tolerance: {THRESHOLD_TOLERANCE_TAU:.2f}). ")

                # Step 2: The Eleastic Buffer
                print(" -> Routing anamalous record to Elastic Buffer.")
                global_elastic_buffer.append(record)

                # Step 3: Autonomous Bifurcation
                if len(global_elastic_buffer) > SATURATION_THRESHOLD_THETA:
                    print(" -> Elastic Buffer saturation threshold reached.")
                    print(" -> Triggering Autonomous Bifurcation.")
                    print(" -> Instantiating new Semantic Centroid and Exact Bounding Region.")

                    # Instantiate emergent prototype
                    emergent_data = np.array(global_elastic_buffer)

                    new_pattern = SemanticPattern(partition_key=p_val)
                    new_pattern.semantic_centroid = np.mean(emergent_data, axis=0)
                    new_pattern.exact_bounding_region = {
                        'min_bounds': np.min(emergent_data, axis=0),
                        'max_bounds': np.max(emergent_data, axis=0)
                    }
                    new_pattern.delta_vectors = [row - new_pattern.semantic_centroid for row in emergent_data]
                    db.partitions[p_val] = [new_pattern]

                    # clear buffer
                    global_elastic_buffer.clear()


    # final system state
    print_section("Final System State", is_subsection=True)
    latest_region = 4
    latest_branch = db.partitions[latest_region][0]

    print(f"New Emergent Prototype (Region {latest_region}):")
    print(f" -> Centroid: {latest_branch.semantic_centroid}")
    print(f" -> Exact Bounding Region Floor (Min): {latest_branch.exact_bounding_region['min_bounds']}")
    print(f" -> Exact Bounding REgion Ceiling (Max): {latest_branch.exact_bounding_region['max_bounds']}")
    print("-" * 60)


if __name__ == "__main__":
    run_level_2()
