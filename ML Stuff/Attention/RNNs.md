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
[[#Gradient Clipping]] can help with exploding gradients, but it did not solve vanishing gradients in deep networks. LSTMs were build for that. The intuition behind the name is
- RNNs have *long-term memory* in the form of weights. They change slowly during training and encode general knowledge about data
- RNNs have *short-term memory* in the form of activations that are passed from each node to the next time step
- The *memory cell* introduces an intermediate type of storage

![[LSTM-memory-cell.png]]

- each *memory cell* has **internal state** $\bf{C}_t$ in addition to the hidden state $\bf{H}_t$ 
- each *memory cell* learns **4** different computations:
	- the **input node** calculates the candidate internal state $\tilde{\bf{C}}_t \in  \mathbb{R}^{n \times h}$ with values in $(-1, 1)$ $$\tilde{\bf{C}}_t = \tanh(\bf{X}_T\bf{W}_{xc} + \bf{H}_{t-1}\bf{W}_{hc} + \bf{b}_c)$$
	- the **forget gate** $\bf{F}_t \in  \mathbb{R}^{n \times h}$ with values in $(0, 1)$ controls if the current value of the "memory" (= internal state) should be kept or deleted ("forgotten") $$\bf{F}_t = \sigma(\bf{X}_t\bf{W}_{xf} + \bf{H}_{t-1}\bf{W}_{hf}+\bf{b}_f))$$
	- the **input gate** $\bf{I}_t \in  \mathbb{R}^{n \times h}$ with values in $(0, 1)$ controls if the candidate internal state should affect the "memory" (=be added tot he internal state) $$\bf{I}_t = \sigma(\bf{X}_t\bf{W}_{xi} + \bf{H}_{t-1}\bf{W}_{hi}+\bf{b}_i))$$
	- the **output gate** $\bf{O}_t \in  \mathbb{R}^{n \times h}$ with values in $(0, 1)$ controls if the memory cell should impact the output of the current step based on its internal state or better rely more on the input alone $$\bf{O}_t = \sigma(\bf{X}_t\bf{W}_{xo} + \bf{H}_{t-1}\bf{W}_{ho}+\bf{b}_o))$$
- **internal state** $\bf{C}_t$ is calculated as $$\bf{C}_t = \bf{F}_t \odot \bf{C}_{t-1} + \bf{I}_t \odot \tilde{\bf{C}}_t$$
	- the forget gate controls the contribution of the internal state from the earlier time step
	- the input gate controls the contribution of the candidate internal state
	- internal state is only passed to the next time step of the same memory cell
- **hidden state** $\bf{H}_t$ is calculated as $$\bf{H}_t = \bf{O}_t \odot \tanh(\bf{C}_t)$$
	- the output gate controls if the current memory impacts other layers of the network or not
	- hidden state is is passed to both the next time step of the same memory cell and the downstream layers of the network!

## GRU - Gated Recurrent Units
Simplify the concepts of LSTM cells to get the same benefits with less computation. It only tracks hidden state (not an additional internal state) and learns only three (not four) calculations.

![[GRU.png]]

- each GRU learns 3 different computations:
	- the **reset gate** $\bf{R}_t \in \mathbb{R}^{n \times h}$ with values in $(0,1)$ controls if we remember the hidden state of the last time step in the calculation of the candidate hidden state or not $$\bf{R}_t = \sigma(\bf{X}_t\bf{W}_{xr} + \bf{H}_{t-1}\bf{W}_{hr}+\bf{b}_r))$$
	- the **update gate** $\bf{Z}_t \in \mathbb{R}^{n \times h}$ with values in $(0,1)$ controls how strongly the new hidden state is updated in this time step or kept as-is $$\bf{Z}_t = \sigma(\bf{X}_t\bf{W}_{xz} + \bf{H}_{t-1}\bf{W}_{hz}+\bf{b}_z))$$
	- the **candidate hidden state** $\tilde{\bf{H}}_t \in \mathbb{R}^{n \times h}$ with values in $(-1, 1)$ is calculated using the reset gate: $$\tilde{\bf{H}}_t = \tanh (\bf{X}_t\bf{W}_{xh} + (\bf{R}_t \odot \bf{H}_{t-1})\bf{W}_{hh} + \bf{b}_h)$$
		- for $\bf{R}_t = 1$ this calculates a vanilla RNN
		- for $\bf{R}_t = 0$ this calculates an MLP with $\bf{X}_t$ as input, ignoring the hidden state
- final **hidden state** is calculated using the update gate: $$\bf{H}_t = \bf{Z}_t \odot \bf{H}_{t-1} + (1-\bf{Z}_t) \odot \tilde{\bf{H}}_t $$
	- for $\bf{Z}_t = 1$ the old state of the last time step is completely retained. This effectively ignores the information from $\bf{X}_t$ and skips time step $t$ in the dependency chain.
	- for $\bf{Z}_t = 0$ the new hidden state is equal to the candidate hidden state.

# Bidirectional RNNs
For tasks like "Fill in the middle", RNNs need to take into account the context of a sequence both before and after the token to predict.

Easiest way to achieve that is to stack two RNNs on top of each other for each layer, on processing the sequence forward and one backward.

![[bidirectional-RNN.png]]

- 

# Training Details

## Gradient Clipping

when backpropagating gradients over time in a sequence, we get an $O(T)$ chain of matrix multiplications. Depending on the properties of the weight matrices, this can lead to vanishing or exploding gradients.

- Generally speaking, we update a parameter $\bf{x}$ by pushing it ini the direction of the negative gradient $\bf{g}$ with a learning rate $\eta > 0$: $$\bf{x} \leftarrow \bf{x} - \eta \bf{g}$$
- The **gradient clipping** heuristic eliminates **exploding** gradients by projecting big gradients onto a ball of radius $\theta$  $$\bf{g} \leftarrow \min \left( 1, \frac{\theta}{\|\bf{g}\|}\right) \bf{g}$$


## Backropagating through time

- calculating gradients back through multiple time steps can lead to exploding / vanishing gradients / numerical instability
- *heuristic* solution: do not calculate the full range of gradient contributions for all time steps, but truncate the calculation after $\tau$ steps.
	- that means the model only accounts for short-term influence