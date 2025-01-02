
# Transformer

![[transformer architecture.png]]

- **Input:** Embeddings + positional encoding
- **Encoder:** 
	- multiple identical layers, each consists of two sublayers:
		- 1st: Multi-head self-attention pooling
		- 2nd: positionwise feed-forward
	- both sublayers are wrapped by a residual connection & layer normalization
	- skip connection requires that output dimension == input dimension for all sublayers
- **Decoder:**
	- multiple identical layers, each consists of three sublayers:
		- 1st: Masked multi-head self-attention (masked because decoder should not know about future)
		- 2nd: encoder-decoder attention: queries are from decoder self-attention, keys & values are from the previous decoder layer
		- 3rd: positionwise feed-forward
- single Attention Head: transforms embedding of input vector to new embedding that attends to different parts of the sequence
- multiple Attention heads in parallel per Attention Block
- multiple layers of Attention Blocks after each other


# Encoder Only - BERT

Bidirectional Encoder Representations from Transformers

- Bidirectional: Encoder is not masked, can attend to all tokens in the sequence
- Encoder creates same-length sequence as input!
- Additional task-specific head needs to be fine-tuned

# Encoder-Decoder - T5

Text-to-Text Transfer Transformer

- allows to generate arbitrary-length sequences
- encoder-decoder cross-attention attends to all input tokens
- *"causal"* attention is masked to only attend to past and present target tokens

# Decoder Only - GPT

Generative Pre-Trained Transformer

- pre-trained via language-modeling (predicting next token in sequence)
- drops encoder blocks and cross-attention layer