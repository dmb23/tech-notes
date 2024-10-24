# Basic Ideas
- Input $\bm{x}$, single neuron of a NN has weights $\bm{w}$ and bias $b$ to get the output $o = \bm{w} \cdot \bm{x} + b$ 
- For a fully-connected layer with vector input and output, this becomes $\bm{o} = \bm{Wx} + \bm{b}$
- update weights and bias via gradient descent
	- measure loss as $l_2$ norm:  $L(\bm{w}, b) =  \| \bm{o} - \bm{y} \|_2^2$ 

## Regularization

Regularization techniques try to avoid overfitting when only limited data is available

- *weight decay:* add the norm of the weight vector to the loss function 

## Activation function

- *softmax* $$\begin{align*} \hat{\bm{y}} &= \text{softmax}(\bm{o}) \\ \hat{y_i} &= \frac{\exp(o_i)}{\sum_j \exp(o_j)} \end{align*}$$
