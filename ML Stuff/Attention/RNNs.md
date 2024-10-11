# Sequence Modelling

- data might be sequential $(x_1, ..., x_T)$  
- Ideal: know how likely we are to see a given sequence:
	- probability mass function $p(x_1, ..., x_T)$
- More realistic: searching to know the probability distribution $P(x_t|x_{t-1}, ..., x_1)$ for the next step
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

## Sequence Models
Language Modelling often consists in evaluating the probability for a given sequence (how good is the output sentence for machine translation). This can be reduced to an autoregressive problem by using a product of conditional densities:

$$ P(x_1, ..., x_T) = P(x_1)\prod_{t=2}^T P(x_t|x_{t-1}, ..., x_1) $$ 
### Markov Models
When we assume that the next step only depends on the recent history, ($\tau$ steps), we arrive at Markov models. For a first-order Markov model ($\tau=1$) the joint probability becomes
$$ P(x_1, ..., x_T) = P(x_1) \prod_{t=2}^T P(x_t|x_{t-1]})$$ 