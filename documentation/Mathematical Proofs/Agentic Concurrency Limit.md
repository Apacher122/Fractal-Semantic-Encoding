# Theorem 1: The Agentic Concurrency Limit (The KV Cache Bottleneck)

**Definitions**

- $V_{total}\in\mathbb{R}^+$ : The total system High-Bandwidht Memory (HBM) capacity.
- $M_{weights}\in\mathbb{R}^+$ : Static memory required to hold model parameters
- ${N}\in\mathbb{Z}^+$ : Sequence length (memory context in tokens)
- $C\in\mathbb{R}^+$ : The architectural constant for memory per token ($C=2*L*H*D*P$, where $L$ is layers, $H$ is attention heads, $D$ is dimension size, and $P$ is precision bytes)
- $U\in\mathbb{Z}^+$ : Number of concurrent homogenous agent instances

**Axiom 1 (Physical Memory Constraint)**:

The total memory allocated by the system cannot exceed the physical hardware capacity.
$V_{total}>M_{weights}$ must hold true for the system to initialize.

**Proof**

1. Let $V_{dyn}=V_{total}-M_w$ represent the strictly positive available dynamic memory for inference.
2. The memory footprint of the KV cache for a single agent is a linear funcction of its context window: $f(N)=C*N$.
3. For a system to successfully support $U$ concurrent agents without an out-of-memory (OOOM) failure, the total dynamic memory allocated must satisfy the following inequality:

$$\sum_{i=1}^{U} f(N) \le V_{dyn}$$

4. Assuming homogenous sequence lengths $N$ across all instances, this summation simplies to:

$$U*(C*N) \le V_{dyn}$$

5. Isolate the concurrency variable $U$ to yield the upper bound constraint:

$$U \le \frac{V_{dyn}}{C*N}$$

6. Therefore, the theoretical maximum concurrency limit ($U_{max}$) is deifned as the floor of the upper bound:

$$U_{max}=\lfloor\frac{V_{dyn}}{C*N}\rfloor$$
