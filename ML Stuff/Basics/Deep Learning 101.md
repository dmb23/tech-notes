---
$$
\newcommad{\bm}[1]{\mathbf{ #1 }}
$$
---
# Basic Ideas
- Input $\vec{x}$ , simple layer of a NN has weights $\vec{w}$ and bias $b$ to get the output $o = \vec{w} \cdot \vec{x} + b$ 
- update weights and bias via gradient descent
	- measure loss as $l_2$ norm:  $L(\vec{w}, b) =  \| \vec{o} - \vec{y} \|_2^2$ 

## Regularization

Regularization techniques try to avoid overfitting when only limited data is available

- *weight decay:* add the norm of the weight vector to the loss function 