# genpark-blackboard-shared-scratchpad-swarm-skill

Agent Skill implementing the **Blackboard Architectural Pattern for Multi-Agent Swarms** in 100% Python standard library.

## Architectural Flow
```mermaid
flowchart TD
    Controller["Orchestrator Agent"] -->|Post Task Requirements| BB["Shared Blackboard State"]
    AgentA["Specialist Agent A (Data)"] -->|Poll & Claim Task| BB
    AgentB["Specialist Agent B (Code)"] -->|Poll & Claim Task| BB
    AgentA -->|Commit Result| BB
    AgentB -->|Commit Result| BB
    BB --> Unified["Consolidated Shared Solution State"]
```
