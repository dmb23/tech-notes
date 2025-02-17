Common applications are "Sequence to sequence", where input and output sequence might be of different length (e.g. Machine Translation).

# Data Processing

- **Batching:** to stack sequences into batches, they are truncated or padded to a fixed length.
	- Length of the original sequence is stored in additional variable
	- Modern processing ideally buckets sequences of similar length into batches to limit padding
- **Tokenization:** for translation tasks word-level tokenization is better than character level. To limit the size of the vocabulary, rare tokens are mapped to the "unknown" token.

# Encoder-Decoder Architecture

>[!INFO] 
>1. An encoder model processes the input sequence and creates a hidden state which "encodes" the content of the input
>2. This hidden state is passed to the decoder model
>3. The decoder model uses the decoder state as additional input, and works as a normal sequence language model otherwise

- Concepts
	- *teacher forcing* - during training the decoder gets the tokens of the target sequence up to the current time step $t'$ as input, while in prediction it will be the the tokens of the predicted sequence
		- alternatively, the decoder can be fed its own predictions for autoregressive predictions, as would happen in inference
	- *passing state* - the encoder transforms an input sequence of variable length into a fixed-shape context variable $\bf{c}$. This variable can be fed to the decoder in each timestep, it can also be used just once for initialization of the decoder hidden state.
	- *embedding layer* - token indices are translated into feature vectors of specified dimension (independent of the vocabulary size). This can also learn to map semantically similar tokens / sequences to similar regions in the vector space.
- Variables
	- single sequence example, batch size 1
	- $x_1, \ldots, x_T$ is the input sequence, $x_t$ is the $t^\text{th}$ token, $\bf{x}_t$ the equivalent feature vector
	- the encoder transforms the feature vector and hidden state into the next hidden state $$\bf{h}_t^{(e)} = \text{enc}(\bf{x}_t, \bf{h}^{(e)}_{t-1})$$
	- Some context variable $\bf{c}$ is created from all hidden states. Easiest example is just take the last hidden state $\bf{h}_T$ $$\bf{c} = q(\bf{h}^{(e)}_1, \ldots, \bf{h}^{(e)}_T)$$
	- $y_1, \ldots, y_{T'}$ is the target output sequence for each time step $t'$
	- the decoder transforms the output sequence, its hidden state and the context variable into the next hidden state $$\bf{h}^{(d)}_{t'} =\text{dec}(y_{t'-1}, \bf{c},\bf{h}^{(d)}_{t'-1})$$
- Dimensions
	- $\bf{V} \in \mathbb{N}$ size of vocabulary
	- $\bf{X} \in \mathbb{R}^{n \times T}$ 
		- batch size $n = 4$
		- sequence length $T = 9$
		- each entry is the index of a token
	- **encoder** is GRU architecture, $l=2$ layers, $h=16$ hidden units, embedding of input into $e$ dimensions
		- embed input as $\tilde{\bf{X}} \in \mathbb{R}^{T \times n \times e}$ 
		- encode into hidden state $\bf{H}^{(e)}_T \in \mathbb{R}^{l \times n \times h}$
		- take output of last layer as context $\bf{c} \in \mathbb{R}^{n \times h}$
	- **decoder** uses same architecture, so it can be initialized with the hidden state of the encoder. A final fully connected layer predicts output tokens
		- embed input as $\tilde{\bf{X}} \in \mathbb{R}^{T \times n \times e}$ 
		- take context from encoder output of last layer, last step $\bf{c} \in \mathbb{R}^{n \times h}$
			- broadcast to all timesteps $\tilde{\bf{c}} \in \mathbb{R}^{T \times n \times h}$
		- concatenate as $\bf{X_c} \in \mathbb{R}^{T \times n \times (e+h)}$
		- encode into hidden state $\bf{H}^{(d)}_T \in \mathbb{R}^{l \times n \times h}$
		- calculate output via last dense layer $\bf{o} \in \mathbb{R}^{n \times T \times V}$


# Strategies

## Loss function with masking

When training on batches, sequences are padded to the same length. The padding tokens should be excluded from the calculation of the loss function, so the loss function should be masked on those tokens.

## Sequence Prediction

How to extract the final sequence from the token-level probabilities that are provided by the model?

- **Greedy Search**
	- Always take the token with the highest probability next.
- **Exhaustive Search**
	- Calculate all scores of all possible sequences. Take the best.
	- Prohibitive in terms of calculation
- **Beam Search**
	- Search a number of $k$ beams in parallel
	- In each step: 
		- explore all possible continuations of the existing sequences
		- select the $k$ best sequences from all those combinations
	- Possible candidates in step $t$ can be dropped in step $t+1$, if no continuation is in the best $k$ samples overall

