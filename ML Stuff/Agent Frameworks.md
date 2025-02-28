
---

# Agents - quick overview

> [!Info] What are AI Agents?
> AI Agents are programs where LLM outputs control the workflow

|Agency Level|Description|How that’s called|Example Pattern|
|---|---|---|---|
|☆☆☆|LLM output has no impact on program flow|Simple Processor|`process_llm_output(llm_response)`|
|★☆☆|LLM output determines an if/else switch|Router|`if llm_decision(): path_a() else: path_b()`|
|★★☆|LLM output determines function execution|Tool Caller|`run_function(llm_chosen_tool, llm_chosen_args)`|
|★★★|LLM output controls iteration and program continuation|Multi-step Agent|`while llm_should_continue(): execute_next_step()`|
|★★★|One agentic workflow can start another agentic workflow|Multi-Agent|`if llm_trigger(): execute_agent()`|


>[!warning] When to use agents
>Only when you absolutely have to!

---

## Agent libraries

Goals:
- easy parsing of tool calling
- memory of what happened before (multi-step agent)
- error logging, retries, ...

Selection:
- LangGraph ![langgraphlogo | 150](https://langchain-ai.github.io/langgraph/static/wordmark_dark.svg)
- LlamaIndex
- smolagents (HF)
- pydantic-ai
# LangChain /  LangGraph

- Abstract interfaces for common usage for different providers (chat model, retriever, tools, ...)
- prompts are first class citizens
- lots of options from big community
- feels very "scripty"

```python
loader = PyPDFLoader(file_path)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter()
splits = text_splitter.split_documents(docs)
embeddings = HuggingFacembeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_store = InMemoryVectorStore(embeddings)
_ = vector_store.add_documents(documents=all_splits)

prompt = hub.pull("rlm/rag-prompt")

retrieved_docs = vector_store.similarity_search(question)
docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
messages = prompt.invoke({"question": "What is love?", "context": docs_content})

llm = init_chat_model("claude-3-5-sonnet-latests", model_provider="anthropic")
response = llm.invoke(messages)

# assert(response.content == "Baby don't hurt me!")
```
### Agents in LangGraph

- USP:
	- persistence of graph state
		- easy interrupts, debugging, human-in-the-loop, time-travel
	- first-class streaming support
- langserve / langsmith as paid services
- graphs defined via nodes / edges

# LlamaIndex

- Rely on nested composition of Abstractions
- Abstract many things far far away
```python
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
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



# SmolAgents

- Code Agents (write Python instead of JSON of method name and arguments)
- low amount of abstraction
- observability via OpenTelemetry 
	- initialize it once, then forget (?)

# PydanticAI

- USP:
	- Type Safety
	- Dependency Injection
		- for Prompts, Tools, Result Validators
	- -> Good debugging
	- Async is first option
- Targeted at Production Level - higher level of complexity and safety
- Lots of Typing
- Allows for different Workflows:
	- Agents
	- Multi-Agents (Agents in Tools)
	- Graph (`pydantic-graph`, independent sister project)


```python
@dataclass
class Deps:
	openai: AsyncOpenAI
	retriever: MyVectorRetriever

rag_agent = Agent(
	'openai:gpt-40',
	 deps_type=Deps,
	 result_type=str,
	 system_prompt="...",	 
)

@rag_agent.tool
async def retrieve(context: RunContext[Deps], search_query: str) -> str:
	"""..."""
	embeddings = context.deps.openai.embeddings.create(search_query)
	docs = context.deps.retriever.retrieve(embeddings)
	return "\n\n".join(docs)

async def run_agent(question: str):
	openai = AsyncOpenAI()
	deps = Deps(openai=openai, retriever = MyVectorRetriever())
	answer = await agent.run(question, deps=deps)
	print(answer.data)


if __name__ == "_main__":
	question = "What is Love?"
	asyncio.run(run_agent(question))
```