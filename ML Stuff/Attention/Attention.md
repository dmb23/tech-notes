**Simile: Database**
Database $D$ with keys $k$ and values $v$ 
e.g. {("Lastname", "Firstname"), ("Eggerton", "Egon")} - When you search (or query $q$) for "Eggerton" you get "Egon", when you search for "Lama" you get no answer, or you get an approximate match "Lastname"

>[!Definition]
>$\text{Attention}(q, D) = \sum_{i=1}^m \alpha(q, k_i)v_i$

- $\alpha(q, k_i)$ are scalar attention weights
- often you create a convex combination ($\sum \alpha = 1, \alpha \geq 0$)
- e.g. normalize $\alpha = \tfrac{\alpha}{\sum\alpha}$ or softmax $\alpha = \tfrac{\exp \alpha}{\sum \exp\alpha}$

-> *attention pooling* just creates a linear combination of the values by some interaction between the query and the keys

