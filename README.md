# Creo-1
### An open-source framework for developing AI Agent Networks

# Enough RAG, time for MOP!
### Message Orchestration Pattern

This repo implements an improvement on the RAG infrastructure, the **Message Orchestration Pattern**, or **MOP**.

This architecture aims to resolve some of the biggest problems for growing and scaling AI Agent systems:
- Efficient agent-to-agent communication
- Ease of adding new independent agents
- Abstractions for integrating with local or cloud based LLM providers
- Abstractions for custom tool calling

We accomplish this operation by implementing a robust message exchange system using a queue service provider. In our examples we will use RabbitMQ, but this is an abstract layer that can be replaced with another provider like Kafka or SQS.

## Scalable Agents
By using a queue, we can create independant and scalable queue consumer agent, wich we can either pool or distribute acrosss compute resources. This allows us to scale each agent role independently. 