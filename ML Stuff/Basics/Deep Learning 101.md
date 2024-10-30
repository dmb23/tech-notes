# Neural Networks

## Basic Setup
- Input $\bm{x}$, single neuron of a NN has weights $\bm{w}$ and bias $b$ to get the output $o = \bm{w} \cdot \bm{x} + b$ 
- For a fully-connected layer with vector input and output, this becomes $\bm{o} = \bm{Wx} + \bm{b}$. If we have $n_{in}$ different features and want to obtain $n_{out}$ different outputs, then 
	- $\bm{o} \in \mathbb{R}^{n_{out}}$
	- $\bm{x} \in \mathbb{R}^{n_{in}}$
	- $\bm{b} \in \mathbb{R}^{n_{out}}$
	- $\bm{W} \in \mathbb{R}^{n_{out} \times n_{in}}$ 
- For using multiple layers, we need to add a nonlinearity to gain anything. Therefore we apply an *activation function* on the output of each layer
## Gradient Descent

- define a *loss function* to measure the quality of the output
	- for this example: *squared error* between prediction and truth $y_i$ is $$l^{(i)}(\bm{w}, b) = \tfrac{1}{2} \left(o^{(i)} - y^{(i)}\right)^2$$ 
- measure loss as sum over all $n$ training examples:  $$L(\bm{w}, b) = \frac{1}{n} \sum_{i=1}^n l^{(i)}(\bm{w}, b) = \frac{1}{n} \sum_{i=1}^n \frac{1}{2} \left( o^{(i)} - y^{(i)} \right)^2$$
	- Which is equivalent up to a constant factor $\tfrac{1}{2n}$  to the squared L2-Norm: $$\| \bm{o} - \bm{y} \|_2^2 = \sqrt{\sum_{i=1}^n \left( o_i - y_i \right)^2}^2$$ 
- take the gradient of the loss wrt weights & biases over a minibatch of $n_b$ samples, subtract a fraction of it $(\eta)$ from the current value: $$(\bm{w}, b) \leftarrow (\bm{w}, b) - \frac{\eta}{n_b}\sum_{j=1}^{n_b} \delta_{(\bm{w},b)}l^{(i)}(\bm{w},b)$$

## Regularization

Regularization techniques try to avoid overfitting when only limited data is available

- *weight decay:* add the norm of the weight vector to the loss function 

## Activation Functions
- **softmax** for single-category classification $\hat{y_i} = \tfrac{\exp(o_i)}{\sum_j \exp(o_j)}$
- **ReLU** $\sigma(x) = \max(x, 0)$


## Loss Functions
- *squared error*, not actually used: $l^{(i)}(\bm{w}, b) = \tfrac{1}{2} \left(o^{(i)} - y^{(i)}\right)^2$
- **cross-entropy loss**, default for classification problems: $l(\bm{y}, \bm{\hat{y}}) = - \sum_i y_i \log \hat{y}_i$

## Initialization

# Classification

- Use One-Hot encoding for $n_{out}$ labels into an $n_{out}$-dim Vector
- Use a matching activation function on the output to arrive at reasonably-contraint results
	- *softmax* for single-category classification $$\begin{align*} \hat{\bm{y}} &= \text{softmax}(\bm{o}) \\ \hat{y_i} &= \frac{\exp(o_i)}{\sum_j \exp(o_j)} \end{align*}$$
- Use a matching loss function: for one-hot encoded label $\bm{y}$ and model prediction $\bm{\hat{y}}$ over $q$ classes
	- *cross-entropy* loss for single-category classification $$\begin{align*} l(\bm{y}, \bm{\hat{y}}) &= - \sum_{i=1}^q y_i \log \hat{y}_i \\ &= - \log \hat{y}_j \quad \text{where $j$ is the true category} \end{align*}$$
