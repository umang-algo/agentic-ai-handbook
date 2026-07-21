# Chapter 12: The Agentic SDK Landscape: Frameworks & Architectures

> 📝 **Coding Handbook**: Practice the code from this chapter → [GitHub: ch12_agentic_sdks](https://github.com/umang/agentic-ai-handbook/tree/main/coding-handbook/ch12_agentic_sdks)

> "In the early days of LLMs, we wrote raw prompt-response loops and hoped for the best. Today, enterprise agents are built on standardized software development kits (SDKs) that manage conversation state, orchestrate multi-agent collaboration, enforce deterministic execution, and persist memory across service crashes. Choosing the right SDK is not a matter of developer preference --- it is a choice of system architecture."




When building autonomous agents, developers rarely write raw API loops from scratch. Instead, they leverage standardized SDKs to structure agent roles, state memory, and transitions.

## The Five SDK Ecosystems

As analyzed in the AI Agent Masterclass, the modern landscape is divided into five dominant ecosystems:

### 1. The Microsoft Ecosystem: AutoGen & Semantic Kernel
Microsoft's SDK landscape is optimized for **Enterprise Orchestration** and **Message-Passing Multi-Agent Collaboration**.

    - **AutoGen (The Collaborative Swarm):** Focuses on the Actor Model of computing. Specialized agents are defined with specific system instructions and communicate via message-passing. A `GroupChatManager` acts as an arbiter, utilizing an LLM or deterministic rules to select the next speaker, allowing complex debates (e.g., CEO, Risk Manager, and Analyst) to run autonomously.
    - **Semantic Kernel:** Focuses on integration. It models LLM capabilities as plugins (native functions or semantic prompts) that can be chained together using planners, making it the choice for integrating with enterprise C# and Python services.


### 2. The LangChain Ecosystem: LangChain & LangGraph
The LangChain ecosystem is the industry standard for stateful, cyclic graphs and customizable retrieval pipelines.

    - **LangChain (Knowledge Grounding/RAG):** Provides standard abstractions for documents, text splitters, vector stores, and retriever interfaces to build retrieval pipelines.
    - **LangGraph (Stateful Graph Orchestration):** Models agents as stateful graphs where nodes are Python functions (agents/tools) and edges define transitions. Unlike linear chains, LangGraph allows cycles (loops), making it perfect for ReAct-style self-healing processes (Chapter 3). It features native state checkpointing for human-in-the-loop approvals.


### 3. Native Provider Tooling: OpenAI & Google Gen AI SDK
Model providers offer optimized native SDKs that bypass third-party framework overhead.

    - **OpenAI Assistants API:** A server-side agent engine. OpenAI hosts the thread history, vector indexes (File Search), and code sandbox, reducing client-side code complexity.
    - **Google Gen AI SDK (Agent Development Kit):** Built natively for Gemini 2.0 models. It provides features like **Search Grounding** (where the model verifies facts against live Google Search indices before responding) and native function-calling with low latency.


### 4. Specialized Open-Source: CrewAI & HuggingFace smolagents
Specialized open-source frameworks focus on usability, roleplay modeling, and lightweight execution.

    - **CrewAI (Role-Playing Collaboration):** Models systems around human organizational metaphors: Crews, Tasks, and Agents. Each agent is given a specific role, backstory, and target goal. It manages transitions (sequential or hierarchical) to build multi-role pipelines.
    - **HuggingFace smolagents (Code-Native Agents):** A shift away from JSON tool-calling. In smolagents, the agent outputs executable Python code directly. The local runtime runs this code inside a secure environment to call tools, reducing parsing errors.


### 5. Enterprise & Low-Code: Dify & n8n
For visual development and rapid enterprise integration, low-code platforms decouple logic from code.

    - **Dify (Headless Agent Engine):** A visual canvas to construct agent flows, prompt templates, and RAG pipelines. Once designed, the agent is exposed via a headless REST API.
    - **n8n (Autonomous Action Layer):** An workflow automation tool with extensive node integrations. n8n allows agents to trigger webhooks, update CRMs, or route alerts through interactive visual nodes.


## Ecosystem Comparison Matrix

The table below summarizes the trade-offs across these agent development ecosystems:

\begin{table}[h!]

\small


\end{table}

## Stateful Agent Graph Architecture

The diagram below represents the unified architecture of a stateful agent graph orchestrator (e.g., LangGraph / AutoGen hybrid model). State is maintained centrally, and transitions are governed by nodes and edge routers.


*Architecture diagram visualizable in the companion handbook implementation.*


## Asynchronous Graph State Serialization

For industrial deployment, agents must survive application crashes. Runtimes resolve this by serializing the execution state graph into a database checkpoint before every node transition, allowing long-running agent flows to resume later without restarting the pipeline.
