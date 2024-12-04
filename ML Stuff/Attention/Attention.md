##### Simile: Database
Database $D$ with keys $k$ and values $v$ 
e.g. {("Lastname", "Firstname"), ("Eggerton", "Egon")} - When you search (or query $q$) for "Eggerton" you get "Egon", when you search for "Lama" you get no answer, or you get an approximate match "Lastname"

## Attention

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

### scaled dot product attention (cheaper kernel)

Make things faster and cheaper to calculate. Drop terms
