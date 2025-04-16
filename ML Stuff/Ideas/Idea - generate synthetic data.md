My new workflow for generating test & validation data for new AI use cases using Reasoning Models like [Google DeepMind](https://www.linkedin.com/company/googledeepmind/) Gemini Flash Thinking, [OpenAI](https://www.linkedin.com/company/openai/) o1, or DeepSeek:  
  
1️⃣ Prompt Reasoning LLM with a short description of the task you want to solve and that it should generate detailed task instructions, including definitions, clear goals, examples, and output format for expert workers.  
  
2️⃣ Refine the task instructions together with the reasoning LLM  
  
3️⃣ Prompt the Reasoning LLM to generate verification samples and include your work instructions, e.g.  
> “You are provided with task instructions for expert workers to classify X. Help me Generate 100 data samples that can be used for verification. Generate them as JSON with a tuple (query, class). Here are the task instructions that are provided to expert workers:”  
  
4️⃣ Manually go through the sample data for validated samples that can be used for tests or few-shot prompting  
  
  
Here are the "task instructions" for my use case to classify "Google Search Queries" (Result of steps 1️⃣ and 2️⃣ ):