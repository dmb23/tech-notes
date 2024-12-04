##### Simile: Database
Database $D$ with keys $k$ and values $v$ 
e.g. {("Lastname", "Firstname"), ("Eggerton", "Egon")} - When you search (or query $q$) for "Eggerton" you get "Egon", when you search for "Lama" you get no answer, or you get an approximate match "Lastname"

## Attention - Basic Concept

*attention pooling* just creates a linear combination of the values by some interaction between the query and the keys

>[!Definition]
>$\text{Attention}(q, D) = \sum_{i=1}^m \alpha(q, k_i)v_i$

- $\alpha(q, k_i)$ are scalar attention weights
- often you create a convex combination ($\sum \alpha = 1, \alpha \geq 0$)
- e.g. normalize $\alpha = \tfrac{\alpha}{\sum\alpha}$ or softmax $\alpha = \tfrac{\exp \alpha}{\sum \exp\alpha}$

![[Attention-calculation.png]]

##### Equivalent: Kernel Density Estimation
For a regression of scalar observations $(x_i, y_i)$ we can set
- **keys** $k_i = x_i$
- **values** $v_i = y_i$
- **query**  $q$ is a location to get an estimate at for the regression

And then attend to some locally weighted average to arrive at an estimate for the queried value, e.g. with a Boxcar kernel $\alpha(q,k) = 1 \text{ if } \|q-k\| \leq 1$ (even though Gaussian kernel is more widely used).
- $f(q) = \sum_i v_i \tfrac{\alpha(q,k_i)}{\sum_j\alpha(q,k_j)}$

This can be done by 
- calculate the kernel values for all training features `x_train` crossed with all validation features `x_val`
- normalize the resulting matrix
- multiply the weight matrix with training labels `y_train`

## Attention Scoring Functions
### scaled dot product attention

Make kernels faster and cheaper to calculate. For queries and keys of the same length, this leads to the dot product attention.

Dropping terms of a gaussian kernel that are bounded leads to the dot product. Normalize the variance by accounting for the input dimension. 
- query $\bf{q} \in \mathbb{R}^d$
- key $\bf{k}_i \in \mathbb{R}^d$
- attention function $$a(\bf{q}, \bf{k}_i) = \bf{q}^\intercal\bf{k}_i / \sqrt{d}$$
- attention weights are normalized via softmax $$\alpha(\bf{q}, \bf{k}_i) = \text{softmax}(a(\bf{q}, \bf{k}_i))$$
> for **different dimensions** between queries and keys, it is possible to construct a matrix to address the mismatch: $\bf{q}^\intercal \bf{Mk}$
### Additive Attention

*Additive Attention* is a different attention scoring function with two advantages:
1. it works for queries and keys with different dimensions
2. the attention is additive, which can save on computations

- query $\bf{q} \in \mathbb{R}^q$
- key $\bf{k}_i \in \mathbb{R}^k$
- additive attention scoring function $$a(\bf{q}, \bf{k}_i) = \bf{w}_v^\intercal \tanh(\bf{W}_qq + \bf{W}_kk) \in \mathbb{R} $$ with hidden dimension $h$ and learnable parameters
	- $\bf{W}_q \in \mathbb{R}^{h \times q}$
	- $\bf{W}_k \in \mathbb{R}^{h \times k}$
	- $\bf{w}_v \in \mathbb{R}^h$

Additive Attention can be interpreted as a two-layer MLP with tanh as activation and no bias terms.

## Bahdanau Attention Mechanism in Seq2Seq models
![[Bahdanau-attention.png]]

