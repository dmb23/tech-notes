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

- **inputs** at time step t as a minibatch $\mathbf{X}_t \in \mathbb{R}^{n \times d}$   
- **hidden layer output** at time step t $\bf{H}_t$ is calculated as $$\bf{H}_t = \phi (\bf{X}_t\bf{W}_{dh} + \bf{H}_{t-1}\bf{W}_{hh} + \bf{b}_h)$$
	- $\bf{H_t} \in \mathbb{R}^{n \times h}$
	- weights $\bf{W}_{dh} \in \mathbb{R}^{d \times h}$, $\bf{b}_{h} \in \mathbb{R}^{h}$  and $\phi$ the activation function
- **output** $\mathbf{O}$ is calculated as $$\bf{O} = \bf{HW}_{hm} + \bf{b}_m)$$  with $\bf{O} \in \mathbb{R}^{n \times m}$, $\bf{W}_{hm} \in \mathbb{R}^{h \times m}$, $\bf{b}_{m} \in \mathbb{R}^{m}$ 
