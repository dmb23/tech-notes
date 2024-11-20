Common applications are "Sequence to sequence", where input and output sequence might be of different length (e.g. Machine Translation).

# Data Processing

- **Batching:** to stack sequences into batches, they are truncated or padded to a fixed length.
	- Length of the original sequence is stored in additional variable
	- Modern processing ideally buckets sequences of similar length into batches to limit padding
- **Tokenization:** for translation tasks word-level tokenization is better than character level. To limit the size of the vocabulary, rare tokens are mapped to the "unknown" token.