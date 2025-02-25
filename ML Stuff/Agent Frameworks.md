#  LangGraph

- sister project to langchain
- 

# LlamaIndex

- Rely on nested composition of Abstractions
- Abstract many things far far away
```python
index = VectorStoreIndex()
retriever = VectorIndexRetriever(index=index)
response_synthesizer = get_response_synthesizer()
query_engine = RetrieverQueryEngine(
	retriever=retriever,
	response_synthesizer=response_synthesizer
)

response = query_engine.query("What is love?")
# assert(response == "Baby don't hurt me!")
```

### LlamaIndex - Agents

- [AgentClasses](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/) & [Tools](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/)
	- blackbox classes, `agent.chat()`
	- tool: simple interface, pre-built options
- [Agentic Abstractions]()
	- routers, query transformations, sub questions
- [Workflow](https://docs.llamaindex.ai/en/stable/understanding/workflows/) 
	- event-driven flow control instead of DAGs
		- steps are connected via input/output
	- global context
	- based on pure python & type annotations (?)


Overall: 
- high level of abstraction
- many options provided, but strict adherence to abstractions

# SmolAgents

# PydanticAI

