TAKucreate an efficient RAG engine to answer not only concrete questions about podcasts, but also asbtract / general / summarization questions

## Ideas

## Graph Model

```mermaid
flowchart
	pn("`**Person**
	- name
	`")
	pod("`**podcast**
	- name
	`")
	t("`**Topics**
	- name`")
	e("`**Episode**
	- id
	- title`")
	s("`**Snippet**
	- id
	- embedding
	- type [chunk/summary]`")
	f("`**FullText**
	- id
	- content`")
	pn -->|"`HOSTS`"| pod
	pn -->|"`TAKES_PART`"| e
	pod -->|"`PROVIDES`"| e
	e -->|"`DISCUSSES`"| t
	s -->|"`DISCUSSES`"| t
	s -->|"`APPEARS_IN`"| e
	s -->|"`HAS_CONTENT`"| f
	e -->|"`HAS_CONTENT`"| f
```

### Vector Index on Embeddings:

```
CREATE VECTOR INDEX moviePlots IF NOT EXISTS
FOR (m:Movie)
ON m.embedding
OPTIONS { indexConfig: {
 `vector.dimensions`: 1536,
 `vector.similarity_function`: 'cosine'
}}
```

```
MATCH (m:Movie {title: 'Godfather, The'})
CALL db.index.vector.queryNodes('moviePlots', 5, m.embedding)
YIELD node AS movie, score
RETURN movie.title AS title, movie.plot AS plot, score
```