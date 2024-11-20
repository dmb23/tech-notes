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
- Variables
	- single sequence example, batch size 1
	- $x_1, \ldots, x_T$ is the input sequence, $x_t$ is the $t^\text{th}$ token, $\bf{x}_t$ the equivalent feature vector
	- the encoder transforms the feature vector and hidden state into the next hidden state $$\bf{h}_t^{(e)} = \text{enc}(\bf{x}_t, \bf{h}^{(e)}_{t-1})$$
	- Some context variable $\bf{c}$ is created from all hidden states. Easiest example is just take the last hidden state $\bf{h}_T$ $$\bf{c} = q(\bf{h}^{(e)}_1, \ldots, \bf{h}^{(e)}_T)$$
	- $y_1, \ldots, y_{T'}$ is the target output sequence for each time step $t'$
	- the decoder transforms the output sequence, its hidden state and the context variable into the next hidden state $$\bf{h}^{(d)}_{t'} =\text{dec}(y_{t'-1}, \bf{c},\bf{h}^{(d)}_{t'-1})$$
- Dimensions
	- $\bf{X} \in \mathbb{R}^{n \times T}$ 
		- batch size $n = 4$
		- sequence length $T = 9$
		- each entry is the index of a token
	- **encoder** is GRU architecture, $l=2$ layers, $h=16$ hidden units, embedding of input into $e$ dimensions
		- embed input as $\tilde{\bf{X}} \in \mathbb{R}^{T \times n \times e}$ 
		- encode into hidden state $\bf{H}_T \in \mathbb{R}^{l \times n \times h}$
		- take output of last layer as context $\bf{c} \in \mathbb{R}^{n \times h}$
	- 
