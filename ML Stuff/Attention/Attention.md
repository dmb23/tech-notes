##### Simile: Database
Database $D$ with keys $k$ and values $v$ 
e.g. {("Lastname", "Firstname"), ("Eggerton", "Egon")} - When you search (or query $q$) for "Eggerton" you get "Egon", when you search for "Lama" you get no answer, or you get an approximate match "Lastname"

## Attention
>[!Definition]
>$\text{Attention}(q, D) = \sum_{i=1}^m \alpha(q, k_i)v_i$

- $\alpha(q, k_i)$ are scalar attention weights
- often you create a convex combination ($\sum \alpha = 1, \alpha \geq 0$)
- e.g. normalize $\alpha = \tfrac{\alpha}{\sum\alpha}$ or softmax $\alpha = \tfrac{\exp \alpha}{\sum \exp\alpha}$

-> *attention pooling* just creates a linear combination of the values by some interaction between the query and the keys

##### Equivalent: Kernel Density Estimation
For a regression of scalar observations $(x_i, y_i)$ we can set
- $k_i = x_i$
- $v_i = y_i$
- $q$ is a location to get an estimate at for the regression
- $f(q) = \sum_i v_i \tfrac{\alpha(q,k_i)}{\sum_j\alpha(q,k_j)}$
And then attend to some locally weighted average, e.g. with a Boxcar kernel $\alpha(q,k) = 1 \text{ if } \|q-k\| \leq 1$ (even though Gaussian kernel is more widely used).

This can be done by calculating the kernel values for all training features `x_train` and all validation features `x_val`, normalize the resulting matrix, and multiply with training labels `y_train`

## Commonly Used
