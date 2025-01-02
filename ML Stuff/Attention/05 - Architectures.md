
# Transformer

![[transformer architecture.png]]

- **Input:** Embeddings + positional encoding
- **Encoder:** multiple identical layers, each consists of two sublayers:
	- 1st: Multi-head self-attention pooling
	- 2nd: 
- single Attention Head: transforms embedding of input vector to new embedding that attends to different parts of the sequence
- multiple Attention heads in parallel per Attention Block
- multiple layers of Attention Blocks after each other