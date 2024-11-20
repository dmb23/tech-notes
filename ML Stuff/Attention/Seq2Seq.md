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

- Variables
	- single sequence example, batch size 1
	- $x_1, \ldots, x_T$ is the input sequence, $x_t$ is the $t^\text{th}$ token, $\bf{x}_t$ the equivalent feature vector
	- the encoder transforms the feature vectore and hidden state into the next hidden state $$\bf{h}_t = \text{enc}(\bf{x}_t, \bf{h}_{t-1})$$
	- Some context variable $\bf{c}$ is created from all hidden states. Easiest example is just take the last hidden state $\bf{h}_T$ $$\bf{c} = q(\bf{h}_1, \ldots, \bf{h}_T)$$
- Dimensions
	- $\bf{X} \in \mathbb{R}^{4 \times 9}$ 
		- batch size 4
		- sequence length 9
	- 
