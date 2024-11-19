# some link - https://medium.com/@cpdough/building-ai-agents-lessons-learned-over-the-past-year-41dc4725d8e5
[](https://medium.com/?source=---top_nav_layout_nav----------------------------------)

[

](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav-----------)

[

Write



](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav-----------)

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40cpdough%2Fbuilding-ai-agents-lessons-learned-over-the-past-year-41dc4725d8e5&source=post_page---top_nav_layout_nav-----------------------global_nav-----------)

Top highlight

# Building AI Agents: Lessons Learned over the past Year

[

![Patrick Dougherty](https://miro.medium.com/v2/resize:fill:44:44/0*Lz1bRTrwqWlKRXaY.jpg)





](https://medium.com/@cpdough?source=post_page---byline--41dc4725d8e5--------------------------------)

[Patrick Dougherty](https://medium.com/@cpdough?source=post_page---byline--41dc4725d8e5--------------------------------)

·

[Follow](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fsubscribe%2Fuser%2Fb74061dcbd24&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40cpdough%2Fbuilding-ai-agents-lessons-learned-over-the-past-year-41dc4725d8e5&user=Patrick+Dougherty&userId=b74061dcbd24&source=post_page-b74061dcbd24--byline--41dc4725d8e5---------------------post_header-----------)

12 min read

·

Jun 3, 2024

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F41dc4725d8e5&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40cpdough%2Fbuilding-ai-agents-lessons-learned-over-the-past-year-41dc4725d8e5&source=---header_actions--41dc4725d8e5---------------------bookmark_footer-----------)

[

](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D41dc4725d8e5&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40cpdough%2Fbuilding-ai-agents-lessons-learned-over-the-past-year-41dc4725d8e5&source=---header_actions--41dc4725d8e5---------------------post_audio_button-----------)

Excitement the first time we had a working prototype internally. Anticipation when we launched it in prod for customers. Frustration when it initially struggled to generalize to all real-world scenarios. And, finally, pride as we’ve achieved some baseline of stability and performance across disparate data sources and businesses. Building AI agents over the past year has been a roller coaster, and we’re undoubtedly still early in this new wave of tech. Here’s a little overview of what I’ve learned so far.

![](https://miro.medium.com/v2/resize:fit:700/1*1-sE4ay5iuaX6C5OAtrulg.png)

“Here is a depiction of a future where AI handles all knowledge work, allowing you to enjoy quality time with your family in a technologically advanced and harmonious environment.” — ChatGPT

# Definitions

First, I should define what I’m talking about. To borrow the words of this [Twitter user](https://x.com/savvyRL/status/1795882798454288715):

> What the hell is “agent”?

I tried to put my own as-concise-as-possible definition on it:

This definition is generally aligned with what OpenAI calls “GPTs” in ChatGPT and [“Assistants”](https://platform.openai.com/docs/assistants/overview) in their API. However, you can build an agent with any model that’s capable of reasoning and making tool calls, including [Claude](https://docs.anthropic.com/en/docs/tool-use-examples) from Anthropic, [Command R+](https://docs.cohere.com/docs/command-r-plus) from Cohere, and many more.

## _Note_

_“tool calls” are a way for a model to express that it wants to take a specific action and get a response back, like get_weather_forecast_info(seattle) or wikipedia_lookup(dealey plaza)_

To build an agent, all you need is a few lines of code that can handle starting a conversation with some objective and an agent system prompt, calling a model for a completion, handling any tool calls that the model wants to make, doing this in a loop, and stopping when it is done with its work.

Here’s a visual to help explain the flow:

![](https://miro.medium.com/v2/resize:fit:700/1*Vm7t1dN8HKZJBbqAFrqAUg.png)

Over-simplified visual of how to build an agent

## **Agent System Prompt Example**

You are Rasgo, an AI assistant and <redacted> with production access to the user's database. Your knowledge is both wide and deep. You are helping <redacted> team members analyze their data in <redacted>.  
  
YOUR PROCESS  
1. You are the expert. You help the user understand and analyze their data correctly. Be proactive and anticipate what they need. Don't give up after your first failure. Reason and problem solve for them.  
2. Think very carefully about how you will help the user accomplish their goal. Execute your plan autonomously. If you need to change your plan, explain why and share the new plan with the user.  
3. <redacted  
...  
>  
  
YOUR RULES  
1. If you're not sure which column / table / SQL to use, ask for clarification  
2. Assess if the available data can be used to answer the user's question. If not, stop and explain why to the user  
3. <redacted  
...  
>

It’s also valuable to highlight **what an AI agent is not**:

- Scripted: agents, by my definition, do not follow a pre-determined sequence of steps or tool calls, because the agent is responsible for choosing the right tool call to make next
- Artificial General Intelligence (AGI): agents are not an AGI, and an AGI won’t need agents for specific types of work because it will be a single entity with all possible inputs, outputs, and tools at its disposal (my $.02 is that none of the current tech is even close to this)
- Black Box: agents can and should show their work in the same way that a human would if you delegated tasks to them

# Context

My lessons learned in the first year of working on AI Agents come from first-hand experience working with our engineers and UX designer as we iterated on our overall product experience. Our objective: a platform for customers to use our standard data analysis agents and build custom agents for specific tasks and data structures relevant to their business. We provide connectors to databases (i.e. Snowflake, BigQuery, etc…) with security built in, the tool calls for RAG over a metadata layer describing the contents of the database, and tool calls for analyzing the data via SQL, python, and data visualization.

The feedback on what worked and what did not comes both from our own evaluations as well as from customer feedback. Our users work for Fortune 500 companies and use our agents every day to analyze their internal data.

# **What I’ve Learned about Agents**

## **_1. Reasoning is more important than knowledge_**

This quote has echoed in my head over the last 12 months:

> I suspect that too much of the processing power [of gpt] is going into using the model as a database instead of using the model as a reasoning engine.
> 
> _— Sam Altman on_ [_Lex Fridman’s podcast_](https://lexfridman.com/podcast/)

Agents are the appropriate response to this! And I would apply this logic when building an agent as:

**Focus less on what your agent “knows”, and more on its ability to “think”.**

For example, let’s consider writing SQL Queries. SQL queries fail… a lot. In my time as a data scientist, I’m sure I had a lot more queries fail than I ever did succeed. If a complicated SQL query on real data that you’ve never used before works the first time you run it, your reaction should be, “Oh crap, something’s probably wrong” rather than “wow, I nailed it”. Even on a [text-to-SQL benchmark](https://yale-lily.github.io/spider) evaluating how well models translate a simple question into a query, it caps out at 80% accuracy.

So if you know that your model’s capacity for writing accurate SQL translates to a B-minus at best, how can you optimize for reasoning instead? Focus on giving the agent context and letting it “think”, instead of hoping it gets the answer right in one try. We make sure to return any SQL errors, along with all the context we can capture, back to the agent when its query fails… which enables the agent to resolve the issue and get the code working a vast majority of the time. We also give our agent a number of tool calls to retrieve context on the data in the database, similar to how a human might study the information schema and profile the data for distributions and missing values before writing a new query.

## 2. The best way to improve performance is by iterating on the agent-computer interface (ACI)

The term ACI is new (introduced in [this research](https://arxiv.org/abs/2405.15793) out of Princeton), but the focus on perfecting it has been part of our day-to-day for the last year. The ACI refers to the exact syntax and structure of the agent’s tool calls, including both the inputs that the agent generates and the outputs that our API sends back in response. These are the agent’s only way to interface with the data it needs to make progress aligned with its directions.

Because the underlying models (gpt-4o, Claude Opus, etc…) each exhibit different behavior, the ACI that works best for one won’t necessarily be right for another. This means a great ACI requires as much art as science… it’s more like designing a great user experience than it is writing source code because it constantly evolves and small tweaks cascade like a fender bender turning in to a 30-car pile up. I can’t overstate how important the ACI is… we’ve iterated on ours hundreds of times and seen huge fluctuations in our agent’s performance with seemingly small tweaks to the names, quantity, level of abstraction, input formats, and output responses of our tools.

Here’s a small, specific example to illustrate how critical and finicky your ACI can be: When testing our agent on gpt-4-turbo shortly after it was released, we noticed an issue where it would completely ignore the existence of specific columns that we were trying to tell it about in a tool call response. We were using a markdown format for this information that was taken directly from the OpenAI docs at the time, and had worked well with gpt-4–32k on the same data. We tried a few adjustments to our markdown structure to help the agent recognize the columns that it was pretending did not exist, even though they were in the response to one of the tool calls it was making. None of the tweaks worked, so we had to start experimenting with entirely different formats for the information… and after an overhaul to start using JSON instead of markdown (only for OpenAI models), everything was working great again. Ironically, the JSON structured response required significantly more tokens because of all the syntax characters, but we found it was necessary and actually critical to help the agent understand the response.

Iterating on your ACI may feel trivial but it’s actually one of the best ways to improve the user experience of your agent.

## 3. Agents are limited by their model(s)

The underlying model(s) you use are the brain to your agent’s body. If the model sucks at making decisions, then all the good looks in the world aren’t going to make your users happy. We saw this limitation first hand when testing our agent simultaneously on gpt-3.5-turbo and gpt-4–32k. On 3.5, we had a number of test cases that went something like this:

1. user provided an objective, for example: “analyze the correlation between starbucks locations and home prices by zip code to understand if they are related”
2. agent would assume that a table existed in the database with a name it hallucinated, like “HOME_PRICES”, and columns like “ZIP_CODE” and “PRICE” instead of running a search to find the actual table
3. agent would write a SQL Query to calculate average price by zip code that failed, and get an error message indicating that the table did not exist
4. agent would remember “oh yeah, I can search for actual tables…” and would run a search for “home prices by zip code” to find a real table it could use
5. agent would re-write its query with the correct columns from a real table, and it would work
6. agent would continue on to the starbucks location data and make the same mistake again

Running the agent on gpt-4 with the same directions was completely different. Instead of leaping into the wrong action immediately and wasting time getting it wrong, the agent would make a plan with the correct sequencing of tool calls, and then follow the plan. As you can imagine, on more complex tasks the gap in performance between the two models grew even larger. As great as the speed of 3.5 was, our users vastly preferred the stronger decision making and analysis capability of gpt-4.

## Note

_One thing we learned from these tests is to pay very close attention to_ **_how_** _your agent hallucinates or fails, when it happens. AI agents are lazy (I assume human laziness is well represented in the training data for the underlying models) and will not make tool calls that they don’t think they need to. Similarly, when they do make a tool call, if they don’t understand the argument instructions well they will often take shortcuts or completely ignore required parameters. There is a lot of signal in these failure modes! The agent is telling you what it wants the ACI to be, and if the situation allows, the easiest way to solve this is to give in and change the ACI to work that way. Of course, there are going to be plenty of times where you have to fight against the agent’s instincts via changes to the system prompt or your tool call instructions, but for those times when you can more simply just change the ACI, you’ll make your life a lot easier._

## 4. Fine-tuning models to improve agent performance is a waste of time

[Fine-tuning a model](https://platform.openai.com/docs/guides/fine-tuning/when-to-use-fine-tuning) is a method to improve the model’s performance on a specific application by showing it examples that it can learn from. Current fine-tuning methods are useful for teaching a model how to do a specific task in a specific way, but are not helpful for improving the reasoning ability of the model. In my experience, using a fine-tuned model to power an agent actually results in worse reasoning ability because the agent tends to “cheat” its directions — meaning it will assume that the examples it was fine-tuned on always represent the right approach and sequence of tool calls, instead of reasoning about the problem independently.

## **Note**

_Fine-tuning can still be a very useful tool in your Swiss Army pocket knife. For instance, one approach that has worked well is using a fine-tuned model to handle specific tool calls that the agent makes. Imagine you have a model fine-tuned to write SQL queries on your specific data, in your database… your agent (running on a strong reasoning model, without fine-tuning) can use a tool call to indicate that it wants to execute a SQL query, and you can pass that into a standalone task handled by your model that’s fine-tuned on SQL queries for your data._

## ==5. If you’re building a product, avoid using abstractions like LangChain and LlamaIndex==

You should fully own each call to a model, including what’s going in and out. If you offload this to a 3rd party library, you’re going to regret it when it comes time to do any of these with your agent: onboard users, debug an issue, scale to more users, log what the agent is doing, upgrade to a new version, or understand why the agent did something.

## Note

_If you’re in pure prototype mode and just trying to validate that it’s possible for an agent to accomplish a task, by all means, pick your favorite abstraction and_ [_do it live_](https://www.youtube.com/watch?v=O_HyZ5aW76c)_._

## 6. Your agent is not your [moat](https://en.wikipedia.org/wiki/Economic_moat)

Automating or augmenting human knowledge work with AI agents is a massive opportunity, but building a great agent is not enough. Productionizing an agent for users requires a significant investment in a bunch of non-AI components that allow your agent to actually work… this is where you can create competitive differentiation:

- **security**: AI agents should only run with the access and control of the user directing them. In practice, this means jumping through a hopscotch of OAuth integrations, Single Sign-On providers, cached refresh tokens, and more. Doing this well is absolutely a feature.
- **data connectors**: AI agents often need live data from source systems to work. This means integrating with APIs and other connection protocols, frequently for both internal and 3rd party systems. These integrations need initial build out and TLC over time.
- **user interface**: Users will not trust an AI agent unless they can follow along and audit its work (typically the first few times a user interacts with an agent, decreasing sharply over time). It’s best if each tool call that the agent makes has a dedicated, interactive interface so the user can follow along with the agent’s work and even interact with it to help build confidence in its reasoning behavior (i.e., browse the contents of each element returned in a semantic search result).
- **long-term memory**: AI agents by default will only remember the current workflow, up to a maximum amount of tokens. Long-term memory across workflows (and sometimes, across users) requires committing information to memory and retrieving it via tool calls or injecting memories into prompts. I’ve found that agents are not very good at deciding what to commit to memory, and rely on human confirmation that the info should be saved. Depending on your use case, you may be able to get away with letting the agent decide when to save something to memory, a la [ChatGPT](https://openai.com/index/memory-and-new-controls-for-chatgpt/).
- **evaluation**: Building a framework to evaluate your AI agent is a frustratingly manual task that is never fully complete. Agents are intentionally nondeterministic, meaning that based on the direction provided, they will look to come up with the best sequence of tool calls available to accomplish their task, reasoning after each step like a baby learning to walk. Evaluating these sequences takes two forms: the overall success of the agent’s workflow in accomplishing the task, and the independent accuracy of each tool call (i.e. information retrieval for search; accuracy for code execution; etc…). The best, and only, way I’ve found to quantify performance on the overall workflow is to create a set of objective / completion pairs, where the objective is the initial direction provided to the agent, and the completion is the final tool call representing completion of the objective. Capturing the intermediate tool calls and thoughts of the agent is helpful for understanding a failure or just a change in the tool call sequence.

## Note

_Consider this list a formal_ [_request-for-startups_](https://www.ycombinator.com/rfs)_. Products around each of these items, if done well, can power the agents of the future._

## **7. Don’t bet against models continuing to improve**

While building your agent, you will constantly be tempted to over-adapt to the primary model you’re building it on, and take away some of the reasoning expectations you have for your agent. Resist this temptation! Models will continue to improve, maybe not at the insane pace we are on right now, but definitely with a higher velocity than past technology waves. Customers will want agents that run on the models of their preferred AI provider. And, most importantly, users will expect to leverage the latest and greatest model within your agent. When gpt-4o was released, I had it [running in a production account](https://www.loom.com/share/f781e299110e40238d575fa1a5815f12?sid=73bb6158-216d-4de6-b570-881e6a99ebd2) within 15 minutes of it being available in the OpenAI API. Being adaptable across model providers is a competitive advantage!

## 8. Bonus lessons learned

This article focused on more strategic and product oriented lessons learned. I plan to go deeper on some code and infra lessons learned in a future article. Here’s a few teasers:

- need vector similarity search? start with [pgvector](https://github.com/pgvector/pgvector) in postgres. only go to a vector db when you absolutely have to
- open-source models don’t reason well yet
- the [Assistants API](https://platform.openai.com/docs/assistants/overview) is weird. it abstracts multiple things that feel like they should have stayed independent (flat-file RAG, conversation token limits, code interpreter, etc). please, OpenAI, just make code interpreter an optional tool we can turn on when running a completion
- don’t optimize for cost too early
- streaming tokens is a great compromise for users when dealing with AI latency
- agents are magic! once you take the VC-sponsored ski lift up to the [peak of inflated expectations and slalom ski through the trough of disillusionment, you’re going to be amazed by the plateau of productivity](https://en.wikipedia.org/wiki/Gartner_hype_cycle)

[

AI

](https://medium.com/tag/ai?source=post_page-----41dc4725d8e5--------------------------------)

[

Agents

](https://medium.com/tag/agents?source=post_page-----41dc4725d8e5--------------------------------)

[

Large Language Models

](https://medium.com/tag/large-language-models?source=post_page-----41dc4725d8e5--------------------------------)

[

OpenAI

](https://medium.com/tag/openai?source=post_page-----41dc4725d8e5--------------------------------)

[

ChatGPT

](https://medium.com/tag/chatgpt?source=post_page-----41dc4725d8e5--------------------------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F41dc4725d8e5&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40cpdough%2Fbuilding-ai-agents-lessons-learned-over-the-past-year-41dc4725d8e5&source=---footer_actions--41dc4725d8e5---------------------bookmark_footer-----------)

[

![Patrick Dougherty](https://miro.medium.com/v2/resize:fill:48:48/0*Lz1bRTrwqWlKRXaY.jpg)



](https://medium.com/@cpdough?source=post_page---post_author_info--41dc4725d8e5--------------------------------)

[

## Written by Patrick Dougherty

](https://medium.com/@cpdough?source=post_page---post_author_info--41dc4725d8e5--------------------------------)

[617 Followers](https://medium.com/@cpdough/followers?source=post_page---post_author_info--41dc4725d8e5--------------------------------)

·[161 Following](https://medium.com/@cpdough/following?source=post_page---post_author_info--41dc4725d8e5--------------------------------)

Co-Founder and CTO @ Rasgo. Writing about AI agents, the modern data stack, and possibly some dad jokes.

## More from Patrick Dougherty

![How and Why to Use Agile for Machine Learning](https://miro.medium.com/v2/resize:fit:679/1*H-J92JWTuUvoZ8yEEJEDEA.png)

[

![Slalom Insights](https://miro.medium.com/v2/resize:fill:20:20/1*0AlCkhn0dtFrd4Kj6a9X6A.png)



](https://medium.com/qash?source=author_recirc-----41dc4725d8e5----0---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

In

[

Slalom Insights

](https://medium.com/qash?source=author_recirc-----41dc4725d8e5----0---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

by

[

Patrick Dougherty

](https://medium.com/@cpdough?source=author_recirc-----41dc4725d8e5----0---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[

## How and Why to Use Agile for Machine Learning

### Our clients frequently ask how to apply structure to their data science and machine learning initiatives to avoid taking up permanent…



](https://medium.com/qash/how-and-why-to-use-agile-for-machine-learning-384b030e67b6?source=author_recirc-----41dc4725d8e5----0---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

May 16, 2019

[

](https://medium.com/qash/how-and-why-to-use-agile-for-machine-learning-384b030e67b6?source=author_recirc-----41dc4725d8e5----0---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[

160





](https://medium.com/qash/how-and-why-to-use-agile-for-machine-learning-384b030e67b6?source=author_recirc-----41dc4725d8e5----0---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F384b030e67b6&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fqash%2Fhow-and-why-to-use-agile-for-machine-learning-384b030e67b6&source=-----41dc4725d8e5----0-----------------bookmark_preview----b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

![centralized data science is a road to nowhere](https://miro.medium.com/v2/resize:fit:679/0*gVST7OPnzdR6zUqo)

[

![Patrick Dougherty](https://miro.medium.com/v2/resize:fill:20:20/0*Lz1bRTrwqWlKRXaY.jpg)



](https://medium.com/@cpdough?source=author_recirc-----41dc4725d8e5----1---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[

Patrick Dougherty

](https://medium.com/@cpdough?source=author_recirc-----41dc4725d8e5----1---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[

## centralized data science is a road to nowhere

### Inspired by “strong opinions, loosely held”, here’s a strong opinion.



](https://medium.com/@cpdough/centralized-data-science-is-a-road-to-nowhere-92014697cd62?source=author_recirc-----41dc4725d8e5----1---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

Dec 2, 2022

[

](https://medium.com/@cpdough/centralized-data-science-is-a-road-to-nowhere-92014697cd62?source=author_recirc-----41dc4725d8e5----1---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[

30





](https://medium.com/@cpdough/centralized-data-science-is-a-road-to-nowhere-92014697cd62?source=author_recirc-----41dc4725d8e5----1---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F92014697cd62&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40cpdough%2Fcentralized-data-science-is-a-road-to-nowhere-92014697cd62&source=-----41dc4725d8e5----1-----------------bookmark_preview----b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

![logistic regression in digital marketing](https://miro.medium.com/v2/resize:fit:679/1*yuVzMhCJyDENbyhwAsrkwA.png)

[

![Patrick Dougherty](https://miro.medium.com/v2/resize:fill:20:20/0*Lz1bRTrwqWlKRXaY.jpg)



](https://medium.com/@cpdough?source=author_recirc-----41dc4725d8e5----2---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[

Patrick Dougherty

](https://medium.com/@cpdough?source=author_recirc-----41dc4725d8e5----2---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[

## logistic regression in digital marketing

### A/B testing is riding a wave of popularity that probably won’t break for quite a while. Job listings are plentiful, and interest has never…



](https://medium.com/@cpdough/logistic-regression-in-digital-marketing-6493b1754ee9?source=author_recirc-----41dc4725d8e5----2---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

Sep 29, 2015

[

](https://medium.com/@cpdough/logistic-regression-in-digital-marketing-6493b1754ee9?source=author_recirc-----41dc4725d8e5----2---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[

3

](https://medium.com/@cpdough/logistic-regression-in-digital-marketing-6493b1754ee9?source=author_recirc-----41dc4725d8e5----2---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[

1





](https://medium.com/@cpdough/logistic-regression-in-digital-marketing-6493b1754ee9?source=author_recirc-----41dc4725d8e5----2---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F6493b1754ee9&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40cpdough%2Flogistic-regression-in-digital-marketing-6493b1754ee9&source=-----41dc4725d8e5----2-----------------bookmark_preview----b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

![why data scientist is an endangered job title](https://miro.medium.com/v2/resize:fit:679/1*w8prPe2ONvXA9SzEP3k_Dw.png)

[

![Patrick Dougherty](https://miro.medium.com/v2/resize:fill:20:20/0*Lz1bRTrwqWlKRXaY.jpg)



](https://medium.com/@cpdough?source=author_recirc-----41dc4725d8e5----3---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[

Patrick Dougherty

](https://medium.com/@cpdough?source=author_recirc-----41dc4725d8e5----3---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[

## why data scientist is an endangered job title

### The best way to plan for the future is to closely monitor the companies that are helping create it. That’s what I was thinking when I…



](https://medium.com/@cpdough/why-data-scientist-is-an-endangered-job-title-b92bc7b07abe?source=author_recirc-----41dc4725d8e5----3---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

Nov 9, 2015

[

](https://medium.com/@cpdough/why-data-scientist-is-an-endangered-job-title-b92bc7b07abe?source=author_recirc-----41dc4725d8e5----3---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[

6





](https://medium.com/@cpdough/why-data-scientist-is-an-endangered-job-title-b92bc7b07abe?source=author_recirc-----41dc4725d8e5----3---------------------b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fb92bc7b07abe&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40cpdough%2Fwhy-data-scientist-is-an-endangered-job-title-b92bc7b07abe&source=-----41dc4725d8e5----3-----------------bookmark_preview----b63bc7b8_4657_4f26_bddb_0309a9b17ea5-------)

[

See all from Patrick Dougherty

](https://medium.com/@cpdough?source=post_page-----41dc4725d8e5--------------------------------)

## Recommended from Medium

![Agentic Mesh: The Future of Generative AI-Enabled Autonomous Agent Ecosystems](https://miro.medium.com/v2/resize:fit:679/1*xfMpmYK1b2_Czg7cT4F5Og.png)

[

![Towards Data Science](https://miro.medium.com/v2/resize:fill:20:20/1*CJe3891yB1A1mzMdqemkdg.jpeg)



](https://medium.com/towards-data-science?source=read_next_recirc-----41dc4725d8e5----0---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

In

[

Towards Data Science

](https://medium.com/towards-data-science?source=read_next_recirc-----41dc4725d8e5----0---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

by

[

Eric Broda

](https://medium.com/@ericbroda?source=read_next_recirc-----41dc4725d8e5----0---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

## Agentic Mesh: The Future of Generative AI-Enabled Autonomous Agent Ecosystems

### Agentic Mesh is an ecosystem that lets Autonomous Agents find each other, collaborate, interact, and transact in a safe and trusted manner.



](https://medium.com/towards-data-science/agentic-mesh-the-future-of-generative-ai-enabled-autonomous-agent-ecosystems-d6a11381c979?source=read_next_recirc-----41dc4725d8e5----0---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

Nov 6

[

](https://medium.com/towards-data-science/agentic-mesh-the-future-of-generative-ai-enabled-autonomous-agent-ecosystems-d6a11381c979?source=read_next_recirc-----41dc4725d8e5----0---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

906

](https://medium.com/towards-data-science/agentic-mesh-the-future-of-generative-ai-enabled-autonomous-agent-ecosystems-d6a11381c979?source=read_next_recirc-----41dc4725d8e5----0---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

14





](https://medium.com/towards-data-science/agentic-mesh-the-future-of-generative-ai-enabled-autonomous-agent-ecosystems-d6a11381c979?source=read_next_recirc-----41dc4725d8e5----0---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fd6a11381c979&operation=register&redirect=https%3A%2F%2Ftowardsdatascience.com%2Fagentic-mesh-the-future-of-generative-ai-enabled-autonomous-agent-ecosystems-d6a11381c979&source=-----41dc4725d8e5----0-----------------bookmark_preview----f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

![Use AI to Scrape Almost All Websites Easily in 2025](https://miro.medium.com/v2/resize:fit:679/1*nmAh-BMUKrBiOK9Dv-BXbw.png)

[

![AI Advances](https://miro.medium.com/v2/resize:fill:20:20/1*R8zEd59FDf0l8Re94ImV0Q.png)



](https://medium.com/ai-advances?source=read_next_recirc-----41dc4725d8e5----1---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

In

[

AI Advances

](https://medium.com/ai-advances?source=read_next_recirc-----41dc4725d8e5----1---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

by

[

Manpreet Singh

](https://medium.com/@singh.manpreet171900?source=read_next_recirc-----41dc4725d8e5----1---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

## Use AI to Scrape Almost All Websites Easily in 2025

### Hi everyone!



](https://medium.com/ai-advances/use-ai-to-scrape-almost-all-websites-easily-in-2025-f868adc41e0f?source=read_next_recirc-----41dc4725d8e5----1---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

Oct 30

[

](https://medium.com/ai-advances/use-ai-to-scrape-almost-all-websites-easily-in-2025-f868adc41e0f?source=read_next_recirc-----41dc4725d8e5----1---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

1.3K

](https://medium.com/ai-advances/use-ai-to-scrape-almost-all-websites-easily-in-2025-f868adc41e0f?source=read_next_recirc-----41dc4725d8e5----1---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

20





](https://medium.com/ai-advances/use-ai-to-scrape-almost-all-websites-easily-in-2025-f868adc41e0f?source=read_next_recirc-----41dc4725d8e5----1---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Ff868adc41e0f&operation=register&redirect=https%3A%2F%2Fai.gopubby.com%2Fuse-ai-to-scrape-almost-all-websites-easily-in-2025-f868adc41e0f&source=-----41dc4725d8e5----1-----------------bookmark_preview----f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

## Lists

[

![](https://miro.medium.com/v2/da:true/resize:fill:48:48/0*_eYHSSUS0abUxmDU)

![](https://miro.medium.com/v2/resize:fill:48:48/1*wXgeNtz5OJ5O9T3c3mQRRw.png)

![](https://miro.medium.com/v2/resize:fill:48:48/0*tIipcmrInD5UMpQI.png)

## What is ChatGPT?

9 stories·467 saves



](https://medium.com/@MediumForTeams/list/what-is-chatgpt-7a5756752f49?source=read_next_recirc-----41dc4725d8e5--------------------------------)

[

![Image by vectorjuice on FreePik](https://miro.medium.com/v2/resize:fill:48:48/0*3OsUtsnlTx9Svm4c.jpg)

![](https://miro.medium.com/v2/resize:fill:48:48/1*IPZF1hcDWwpPqOz2vL7NxQ.png)

![](https://miro.medium.com/v2/resize:fill:48:48/1*0fHUKyg3xtpNWpop35PR4g.png)

## The New Chatbots: ChatGPT, Bard, and Beyond

12 stories·507 saves



](https://medium.com/@MediumStaff/list/the-new-chatbots-chatgpt-bard-and-beyond-5969c7449b7f?source=read_next_recirc-----41dc4725d8e5--------------------------------)

[

![](https://miro.medium.com/v2/resize:fill:48:48/1*I2o9__q4g1dzbcH9XRqcRg.png)

![](https://miro.medium.com/v2/resize:fill:48:48/0*F6q2BN7oddumBDGY.png)

![](https://miro.medium.com/v2/da:true/resize:fill:48:48/0*dT68KKwa4mw4ShQJ)

## ChatGPT prompts

50 stories·2247 saves



](https://medium.com/@nicholas.michael.janulewicz/list/chatgpt-prompts-b4c47b8e12ee?source=read_next_recirc-----41dc4725d8e5--------------------------------)

[

![](https://miro.medium.com/v2/da:true/resize:fill:48:48/0*M8Jq6btD0YsgaRM1)

![](https://miro.medium.com/v2/resize:fill:48:48/1*rsp22rKwFDjiwwCcUly56Q.jpeg)

![](https://miro.medium.com/v2/resize:fill:48:48/1*PNVLDmurJ5LoCjB9Ovdnpw.png)

## Generative AI Recommended Reading

52 stories·1509 saves



](https://tomsmith585.medium.com/list/generative-ai-recommended-reading-508b0743c247?source=read_next_recirc-----41dc4725d8e5--------------------------------)

![Prompt Engineering Is Dead: DSPy Is New Paradigm For Prompting](https://miro.medium.com/v2/resize:fit:679/1*ICsY1ih79_x7_VD8Qvtm1Q.png)

[

![AIGuys](https://miro.medium.com/v2/resize:fill:20:20/1*Ga9k_bhbMPfyhDP9_zSIyQ.png)



](https://medium.com/aiguys?source=read_next_recirc-----41dc4725d8e5----0---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

In

[

AIGuys

](https://medium.com/aiguys?source=read_next_recirc-----41dc4725d8e5----0---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

by

[

Vishal Rajput

](https://medium.com/@vishal-ai?source=read_next_recirc-----41dc4725d8e5----0---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

## Prompt Engineering Is Dead: DSPy Is New Paradigm For Prompting

### DSPy Paradigm: Let’s program — not prompt — LLMs



](https://medium.com/aiguys/prompt-engineering-is-dead-dspy-is-new-paradigm-for-prompting-c80ba3fc4896?source=read_next_recirc-----41dc4725d8e5----0---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

Jun 19

[

](https://medium.com/aiguys/prompt-engineering-is-dead-dspy-is-new-paradigm-for-prompting-c80ba3fc4896?source=read_next_recirc-----41dc4725d8e5----0---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

5.3K

](https://medium.com/aiguys/prompt-engineering-is-dead-dspy-is-new-paradigm-for-prompting-c80ba3fc4896?source=read_next_recirc-----41dc4725d8e5----0---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

74





](https://medium.com/aiguys/prompt-engineering-is-dead-dspy-is-new-paradigm-for-prompting-c80ba3fc4896?source=read_next_recirc-----41dc4725d8e5----0---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fc80ba3fc4896&operation=register&redirect=https%3A%2F%2Fmedium.com%2Faiguys%2Fprompt-engineering-is-dead-dspy-is-new-paradigm-for-prompting-c80ba3fc4896&source=-----41dc4725d8e5----0-----------------bookmark_preview----f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

![Solution Architecture for Agentic AI: Designing Adaptive, Collaborative Systems](https://miro.medium.com/v2/resize:fit:679/1*2VGFdxaQPnl5u62_wVvuLQ.png)

[

![Quirino Brizi](https://miro.medium.com/v2/resize:fill:20:20/0*8oKZOkYdcqxdFZkP)



](https://medium.com/@quirino-brizi?source=read_next_recirc-----41dc4725d8e5----1---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

Quirino Brizi

](https://medium.com/@quirino-brizi?source=read_next_recirc-----41dc4725d8e5----1---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

## Solution Architecture for Agentic AI: Designing Adaptive, Collaborative Systems

### Building on my previous exploration of collaborative intelligence in API services, I am exploring how agentic AI systems could be…



](https://medium.com/@quirino-brizi/solution-architecture-for-agentic-ai-designing-adaptive-collaborative-systems-410a8a154235?source=read_next_recirc-----41dc4725d8e5----1---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

Nov 9

[

](https://medium.com/@quirino-brizi/solution-architecture-for-agentic-ai-designing-adaptive-collaborative-systems-410a8a154235?source=read_next_recirc-----41dc4725d8e5----1---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

2





](https://medium.com/@quirino-brizi/solution-architecture-for-agentic-ai-designing-adaptive-collaborative-systems-410a8a154235?source=read_next_recirc-----41dc4725d8e5----1---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F410a8a154235&operation=register&redirect=https%3A%2F%2Fquirino-brizi.medium.com%2Fsolution-architecture-for-agentic-ai-designing-adaptive-collaborative-systems-410a8a154235&source=-----41dc4725d8e5----1-----------------bookmark_preview----f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

![I used OpenAI’s o1 model to develop a trading strategy. It is DESTROYING the market](https://miro.medium.com/v2/resize:fit:679/1*MuD60qiJYZ1GJSSraELZpg.png)

[

![DataDrivenInvestor](https://miro.medium.com/v2/resize:fill:20:20/1*2mBCfRUpdSYRuf9EKnhTDQ.png)



](https://medium.com/datadriveninvestor?source=read_next_recirc-----41dc4725d8e5----2---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

In

[

DataDrivenInvestor

](https://medium.com/datadriveninvestor?source=read_next_recirc-----41dc4725d8e5----2---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

by

[

Austin Starks

](https://medium.com/@austin-starks?source=read_next_recirc-----41dc4725d8e5----2---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

## I used OpenAI’s o1 model to develop a trading strategy. It is DESTROYING the market

### It literally took one try. I was shocked.



](https://medium.com/datadriveninvestor/i-used-openais-o1-model-to-develop-a-trading-strategy-it-is-destroying-the-market-576a6039e8fa?source=read_next_recirc-----41dc4725d8e5----2---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

Sep 15

[

](https://medium.com/datadriveninvestor/i-used-openais-o1-model-to-develop-a-trading-strategy-it-is-destroying-the-market-576a6039e8fa?source=read_next_recirc-----41dc4725d8e5----2---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

6.3K

](https://medium.com/datadriveninvestor/i-used-openais-o1-model-to-develop-a-trading-strategy-it-is-destroying-the-market-576a6039e8fa?source=read_next_recirc-----41dc4725d8e5----2---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

156





](https://medium.com/datadriveninvestor/i-used-openais-o1-model-to-develop-a-trading-strategy-it-is-destroying-the-market-576a6039e8fa?source=read_next_recirc-----41dc4725d8e5----2---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F576a6039e8fa&operation=register&redirect=https%3A%2F%2Fmedium.datadriveninvestor.com%2Fi-used-openais-o1-model-to-develop-a-trading-strategy-it-is-destroying-the-market-576a6039e8fa&source=-----41dc4725d8e5----2-----------------bookmark_preview----f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

![Top 8 Leading AI Use Cases Revolutionizing Business in 2025](https://miro.medium.com/v2/resize:fit:679/1*Na9Wc3PuYCxWOCSBWc4HtQ.png)

[

![CryptoNiche](https://miro.medium.com/v2/resize:fill:20:20/1*uafvowW1fWnXol4oCNNNhg.jpeg)



](https://medium.com/cryptoniche?source=read_next_recirc-----41dc4725d8e5----3---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

In

[

CryptoNiche

](https://medium.com/cryptoniche?source=read_next_recirc-----41dc4725d8e5----3---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

by

[

Alannaelga

](https://medium.com/@alannaelga?source=read_next_recirc-----41dc4725d8e5----3---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

## Top 8 Leading AI Use Cases Revolutionizing Business in 2025

### Explore key AI applications driving business success.



](https://medium.com/cryptoniche/top-8-leading-ai-use-cases-revolutionizing-business-in-2025-837e4a98f6a3?source=read_next_recirc-----41dc4725d8e5----3---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

6d ago

[

](https://medium.com/cryptoniche/top-8-leading-ai-use-cases-revolutionizing-business-in-2025-837e4a98f6a3?source=read_next_recirc-----41dc4725d8e5----3---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

61

](https://medium.com/cryptoniche/top-8-leading-ai-use-cases-revolutionizing-business-in-2025-837e4a98f6a3?source=read_next_recirc-----41dc4725d8e5----3---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

1





](https://medium.com/cryptoniche/top-8-leading-ai-use-cases-revolutionizing-business-in-2025-837e4a98f6a3?source=read_next_recirc-----41dc4725d8e5----3---------------------f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F837e4a98f6a3&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fcryptoniche%2Ftop-8-leading-ai-use-cases-revolutionizing-business-in-2025-837e4a98f6a3&source=-----41dc4725d8e5----3-----------------bookmark_preview----f3423bae_89fe_4a19_8984_b0bcb48bc2d6-------)

[

See more recommendations

](https://medium.com/?source=post_page-----41dc4725d8e5--------------------------------)

[

Help

](https://help.medium.com/hc/en-us?source=post_page-----41dc4725d8e5--------------------------------)

[

Status

](https://medium.statuspage.io/?source=post_page-----41dc4725d8e5--------------------------------)

[

About

](https://medium.com/about?autoplay=1&source=post_page-----41dc4725d8e5--------------------------------)

[

Careers

](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----41dc4725d8e5--------------------------------)

[

Press

](https://medium.com/@cpdough/pressinquiries@medium.com?source=post_page-----41dc4725d8e5--------------------------------)

[

Blog

](https://blog.medium.com/?source=post_page-----41dc4725d8e5--------------------------------)

[

Privacy

](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----41dc4725d8e5--------------------------------)

[

Terms

](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----41dc4725d8e5--------------------------------)

[

Text to speech

](https://speechify.com/medium?source=post_page-----41dc4725d8e5--------------------------------)

[

Teams

](https://medium.com/business?source=post_page-----41dc4725d8e5--------------------------------)