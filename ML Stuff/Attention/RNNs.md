# Sequence Modelling

- data might be sequential $(x_1, ..., x_T)$  
- searching to know the probability distribution $P(x_t|x_{t-1}, ..., x_1)$
- possible: apply linear regression to estimate the condiiton expectation $\mathbb{E}[(x_t | x_{t-1}, ..., x_1)]$   

>[!autoregressive models]
> regress the value of the next step based on the values of the same variable before

- variable sequence length for input is annoying
- you can only look at $\tau$ values in the past
- you can keep track of the history in a hidden state $h_t$
	- then you estimate based on the hidden state $\hat{x}_t = P(x_t | h_t)$
	- and update the hidden state each step $h_t = g(h_{t-1}, x_{t-1})$

>[!Latent Autoregressive Models:]
> an autoregressive model that carries a latent state to keep track of history

- when estimating the next value in a sequence, we assume the value will fluctuate, but the dynamics after which it is created are stable. Those are **stationary** dynamics.
