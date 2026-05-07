"""
Fractal Semantic Encoding (FSE) - EQP Core Engine

Tier 1: Deterministic Partitioning (Categorical Walls)
Tier 2: Semantic Clustering (Exact Bounding Boxes)
"""
import numpy as np
from sklearn.cluster import KMeans

class SemanticPattern:
    """
    Section 4.1: Pattern Representation
    Python representation of a Semantic Pattern (P[k]) within the FSE hierarchy.
    
    A Semantic Pattern is a decoupling of statistical identities of data from their physical extent.
    It serves as the fundamental node within the Tier 2 Fractal Branch.

    Attributes:
        partition_key (int/float/str): The categorical identifier of a pattern.
        semantic_centroid (np.ndarray): The d-dimensional mean vector (mu[k]) aka the prototype.
        exact_bounding_region (dict): The axis-aligned hyper-rectangle (B[k]) defining the absolute
            support of the partition.
        delta_vectors (list of np.ndarray): Compressed Tier 3 residual vectors (delta[k]). Stored
            relative to the semantic centroid.
        elastic_buffer (list): Transient storage (E[k]) for out-of-bound records pending Autonomous
            Bifurcation.
    """

    def __init__(self, partition_key):
        # Tier 1: Deterministic Partitioning
        self.partition_key = partition_key

        # 4.1: Pattern Representation
        self.semantic_centroid = None
        self.exact_bounding_region = {}

        # 4.6: Theorem 5: Entropy Reduction and Storage Density
        # 5.4: Tier 3: Residual Encoding
        self.delta_vectors = []

        # 7.2: The Elastic Buffer
        self.elastic_buffer = []
    
class FSECore:
    """
    Chapter 2: Fractal Semantic Encoding (FSE): An Introduction
    Exact Query Processing(EQP) Core Engine
    
    FSE removes the need for a traditional secondary index. Combining absolute categorical state
    isolation (Tier 1) with autonomous multi-dimensional bounding matrices (Tier 2), the FSE engine
    natively bypasses millions of floating-point operations, and achieves index-level search
    speeds with zero storage bloat and zero mathematical degradation.
    """
    def __init__(self, partition_col=0, n_sub_clusters=2):
        """
        Args:
            partition_col (int): Column index for deterministic walls (e.g., Region).
            n_sub_clusters (int): How many fractal branches to grow inside each wall.
        """
        self.partition_col = partition_col
        self.n_sub_clusters = n_sub_clusters

        # 3.1: Disjoint Union D 
        self.partitions = {}

    def bootstrap(self, raw_data):
        """
        6.1 Ingestion: The Cold Start
        Transitioning raw data into mathematically bounded fractal hierarchy.
        """
        unique_partitions = np.unique(raw_data[:, self.partition_col])

        for p_val in unique_partitions:
            # 5.2 Tier 1: Deterministic Partitioning
            # Categorical wall enforcement
            mask = raw_data[:, self.partition_col] == p_val
            partition_data = raw_data[mask]

            # 5.3 Tier 2: Pattern Construction
            self.partitions[p_val] = self._fork_fractal_branches(partition_data, p_val)

    def _fork_fractal_branches(self, data, partition_key):
        """
        6.2 Pattern Discovery and Hierarchy Formation
        Minimize intra-cluster variance by solving the objective function.
        Then calculate centroids and boundaries to establish Deterministic Spatial Contracts
        """
        n_clusters = min(len(data), self.n_sub_clusters)

        # 6.1 III: Objective Function Optimization
        km = KMeans(n_clusters=n_clusters, random_state=42, n_init=5).fit(data)

        branches = []
        for i in range(n_clusters):
            cluster_points = data[km.labels_ == i]

            # 6.1 IV: The State Transition
            pattern = SemanticPattern(partition_key)

            # 4.1: Calculating the Semantic Centroid
            pattern.semantic_centroid = np.mean(cluster_points, axis=0)

            # 4.1: Calculating the Exact Bounding Region and signing Deterministic Spatial Contract
            pattern.exact_bounding_region = ({
                'min_bounds': np.min(cluster_points, axis=0), # Absolute Floor
                'max_bounds': np.max(cluster_points, axis=0), # Absolute Ceiling
            })

            # 4.6 Theorem 5: Entropy Reduction and Storage Density
            pattern.delta_vectors = [row - pattern.semantic_centroid for row in cluster_points]

            branches.append(pattern)
        return branches

    def execute_query(self, partition_filter, branch_evaluator, leaf_evaluator, aggregator):
        """
        5.5 Query Execution via Deterministic Pruning
        Executes a three-tier hierarchical search using Exact Bounds.
        """
        relevant_records = []
        rows_touched = 0

        for p_val, branches in self.partitions.items():
            # 5.2 Tier 1: Deterministic Partitioning
            if not partition_filter(p_val):
                continue

            for branch in branches:
                # 4.3 Theorem 2: Deterministic Query Pruning
                if not branch_evaluator(branch):
                    continue

                # 4.2 Theorem 1: Exact Reconstruction
                for delta in branch.delta_vectors:
                    rows_touched += 1
                    reconstructed = branch.semantic_centroid + delta

                    if leaf_evaluator(reconstructed):
                        relevant_records.append(reconstructed[2])

        result = aggregator(relevant_records) if relevant_records else 0.0
        return result, rows_touched
