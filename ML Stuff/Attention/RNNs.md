- If we rely on **Markov models** to capture the effect of all preceding timesteps in a sequence on the prediction of a token $x_t$, then the **number of model parameters increases exponentially** 
	- If the probability of a specific n-gram is a parameter, then you need $|V|^n$ parameters ($V$ is the vocabulary). To condition the Probability of $x_t$ on all preceding elements $x_{t-1}, \ldots, x_0$ you need to account for $t$-grams.
- **latent models** are to be preferred, they can capture the effects of all preceding time steps with constant compute / storage 
	- for a hidden state $h_t = f(x_t, h_{t-1})$ a latent model does not need to be an approximation. If $f$ is sufficiently powerful it could store all observed data.
# Reminder: NN without hidden state

**MLP with a single layer**
- **input** as a minibatch $\bf{X} \in \mathbb{R}^{n \times d}$ , batch size $n$ and input size $d$
- **hidden layer** output $\bf{H}$ is calculated as $$\bf{H} = \phi (\bf{XW}_{dh} + \bf{b}_h)$$ with $\bf{H} \in \mathbb{R}^{n \times h}$, $\bf{W}_{dh} \in \mathbb{R}^{d \times h}$, $\bf{b}_{h} \in \mathbb{R}^{h}$  and $\phi$ the activation function
- **output** $\mathbf{O}$ is calculated as $$\bf{O} = \bf{HW}_{hm} + \bf{b}_m)$$  with $\bf{O} \in \mathbb{R}^{n \times m}$, $\bf{W}_{hm} \in \mathbb{R}^{h \times m}$, $\bf{b}_{m} \in \mathbb{R}^{m}$ 
- Use e.g. softmax for final classification

# Recurrent NN with hidden state

![[RNN-single-layer.png]]

- **inputs** at time step t as a minibatch $\mathbf{X}_t \in \mathbb{R}^{n \times d}$   
- **hidden layer output** at time step t $\bf{H}_t$ is calculated as $$\bf{H}_t = \phi (\bf{X}_t\bf{W}_{dh} + \bf{H}_{t-1}\bf{W}_{hh} + \bf{b}_h)$$
	- $\bf{H_t} \in \mathbb{R}^{n \times h}$
	- weights $\bf{W}_{xh} \in \mathbb{R}^{d \times h}$ as weights for the input
	- weights $\bf{W}_{hh} \in \mathbb{R}^{h \times h}$ as weights for the hidden state of the previous time step
	- bias $\bf{b}_{h} \in \mathbb{R}^{h}$
	- and $\phi$ the activation function
- **output** $\mathbf{O}$ is calculated as $$\bf{O} = \bf{HW}_{hm} + \bf{b}_m$$  with $\bf{O} \in \mathbb{R}^{n \times m}$, $\bf{W}_{hm} \in \mathbb{R}^{h \times m}$, $\bf{b}_{m} \in \mathbb{R}^{m}$ 


# Deep RNNs

To build "deep" RNNs the simple approach is to stack RNNs on top of each other: Given a sequence of length $T$, the first RNN produces a sequence of outputs, also of length $T$. These, in turn, constitute the inputs to the next RNN layer.

![[Deep-RNN.png]]
- **inputs** at time step t as a minibatch $\mathbf{X}_t \in \mathbb{R}^{n \times d}$   
	- $t \in [0, T]$ timestep
	- $n$ number of examples in the minibatch
	- each example of dimension $d$ 
- **hidden layer output** of the $l^{\text{th}}$ hidden layer at time step $t$ $\bf{H}^{(l)}_t$ is calculated as $$\bf{H}^{(l)}_t = \phi_l (\bf{H}^{(l-1)}_t\bf{W}^{(l)}_{xh} + \bf{H}^{(l)}_{t-1}\bf{W}^{(l)}_{hh} + \bf{b}^{(l)}_h)$$
	- $\bf{H}^{(l)}_t \in \mathbb{R}^{n \times h}$
		- all hidden layers have number of hidden units $h$
		- (technically some adjustment needed for $\bf{H}^{(0)}_t := \bf{X}_t$ to make things work)
	- weights $\bf{W}^{(l)}_{xh} \in \mathbb{R}^{h \times h}$ as weights for the input (which is then also hidden state of the previous layer)
	- weights $\bf{W}^{(l)}_{hh} \in \mathbb{R}^{h \times h}$ as weights for the hidden state of the previous time step in the same layer
	- bias $\bf{b}^{(l)}_{h} \in \mathbb{R}^{h}$
	- and $\phi_L$ the activation function
- **output** $\mathbf{O}$ is calculated based on the hidden state of the final $L^{\text{th}}$ layer as $$\bf{O}_t = \bf{H}^{(L)}_t \bf{W}_{hm} + \bf{b}_m$$  with $\bf{O} \in \mathbb{R}^{n \times m}$, $\bf{W}_{hm} \in \mathbb{R}^{h \times m}$, $\bf{b}_{m} \in \mathbb{R}^{m}$ 

# Modern RNN Cells
## LSTM - Long Short-Term Memory


# Training Details

## Gradient Clipping

when backpropagating gradients over time in a sequence, we get an $O(T)$ chain of matrix multiplications. Depending on the properties of the weight matrices, this can lead to vanishing or exploding gradients.

- Generally speaking, we update a parameter $\bf{x}$ by pushing it ini the direction of the negative gradient $\bf{g}$ with a learning rate $\eta > 0$: $$\bf{x} \leftarrow \bf{x} - \eta \bf{g}$$
- The **gradient clipping** heuristic eliminates **exploding** gradients by projecting big gradients onto a ball of radius $\theta$  $$\bf{g} \leftarrow \min \left( 1, \frac{\theta}{\|\bf{g}\|}\right) \bf{g}$$


## Backropagating through time

- calculating gradients back through multiple time steps can lead to exploding / vanishing gradients / numerical instability
- *heuristic* solution: do not calculate the full range of gradient contributions for all time steps, but truncate the calculation after $\tau$ steps.
	- that means the model only accounts for short-term influence