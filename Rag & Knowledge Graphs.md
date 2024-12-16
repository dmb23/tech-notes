# GraphRAG

[Arxiv Paper](https://arxiv.org/pdf/2404.16130)
[GraphRAG github](https://github.com/microsoft/graphrag) (quite complicated)
[nano-graphrag](https://github.com/gusye1234/nano-graphrag), a simple, easy-to-hack GraphRAG implementation

![[GraphRAG-overview.png]]

## GraphRAG Pipeline

1. create chunks
	- smaller chunks extract more entities
	- bigger chunks are cheaper (need less LLM calls)
2. Extract Graph Information
	1. Extract all entities in a chunk
		1. Name, Type, Description
	2. Extract all Relationships between entities in a chunk
	3. **Bonus:** few-shot should improve handling of specific domains!
	4. **Bonus:** ask the LLM if it should go over the chunk again ("gleaning"), then chunk size can be larger
	5. **Optional[?]** Extract claims linked to detected entities
3. 