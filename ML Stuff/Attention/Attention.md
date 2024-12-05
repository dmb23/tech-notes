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

> [!WARNING]
> This attention mechanism does not have any trainable weights!


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

> [!HINT] Key Idea
> Dynamically update the context variable $\bf{c}$ as a function of the original text (encoder hidden state $\bf{h}^{(e)}$) and the text that was already generated (decoder hidden state $\bf{h}^{(d)}$)

- Given an input sequence of length $T$
- at each decoding time step $t'$ update the context $$\bf{c}_{t'} = \sum_{t=1}^T \alpha(\bf{h}_{t'-1}^{(d)}, \bf{h}_t^{(e)}\bf{h}_t^{(e)}$$
	- query is decoder hidden state of last time step $\bf{h}_{t'-1}^{(d)}$
	- keys are the encoder hidden states of all input sequence steps $\bf{h}_{t}^{(e)}$
	- values are also the encoder hidden states
- this context $\bf{c}_{t'}$ is then used to calculate new decoder state $\bf{h}_{t'}^{(d)}$ and to generate a new token

A possible extension is to not stop at $T$ but proceed to $t'-1$ in the attention sum, and take the already generated tokens in the decoder as further context.


## Multi-head attention

![[multihead-attention.png]]

> [!HINT] Key Idea
> Multiple Attention Mechanisms might be able to capture different dependencies (e.g. short-range vs longer-range). So let's combine them

- learn different attention weights and combine them:
	- each attention pooling output is called a head
- to allow the heads to learn different features, transform queries, keys, and values by a linear projection (fully-connected layer)
- final output is another linear projection on the concatenation of all attention head outputs

**NOTE:** This allows also to use [[#scaled dot product attention]] and learn the layer.


## Self-Attention

> [!HINT] Key Idea
> Given a sequence of tokens, this sequence can be used as all **key, query** and **value** in attention pooling.

The self-attention of a sequence $\bf{x}_1, \ldots, \bf{x}_n$ outputs a sequence of the same length $\bf{y}_1, \ldots, \bf{y}_n$, where $$\bf{y}_i = f(\bf{x}_i, D) \qquad \text{where } D = (\bf{x}_1, \bf{x}_1), \ldots, (\bf{x}_n, \bf{x}_n)$$
- self-attention can be computed in parallel for a full sequence, the need for sequential processing as in RNNs is lost
- computation increases quadratically with sequence length, making long sequences expensive (prohibitive?)

### Positional Encoding

Self-Attention can attend to different parts of the input sequence, but does not have any information about the order of the tokens.

This information can be added by positional encodings.
- positional encodings can be learned, or calculated as fixed values
- e.g. sin/cos frequencies of the position with different frequencies
- positional encodings are added to the input embeddings
	- positional encodings must be of the same dimension as the embeddings
