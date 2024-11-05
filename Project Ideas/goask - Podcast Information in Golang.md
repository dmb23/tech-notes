# Vision
Ask any question about your favourite Podcast. Get it answered

# Key Ideas
- **Useful** - create an app around it. Make it easy to distribute.
- **Find episodes** - ask for guests, topics, whatever
- **Get answers** - ask for details that were discussed in the podcast
## Technical Ideas
- Build an App in Golang
- Interact with Podcast metadata
	- find RSS feed via itunes / ...
	- get metadata from RSS feed
	- search through metadata (BOW, Embeddings, ...)
- Interact with Podcast Episodes
	- download, convert, transcribe
- Get questions answered
	- route questions to an LLM
	- feed Podcast content into the LLM
- Idea: allow an Agent model to orchestrate all these options, depending on the question.