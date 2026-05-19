# Assignment 2 — Part 1: ReAct Agent from Scratch

A Python-based ReAct agent built entirely from scratch, without relying on any pre-existing agent frameworks or products. The agent reasons about software engineering tasks and executes them through bash commands using a hand-built reasoning loop.

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Usage](#usage)
- [Security](#security)
- [Constraints](#constraints)

## Overview

This project implements a ReAct (Reasoning + Acting) agent that takes a software engineering task from the user, reasons about what bash command is needed, executes it with user approval, reads the result, and continues until the task is complete.

The agent uses the **OpenAI API** (GPT-4o) as its language model. All surrounding logic — the reasoning loop, output parser, bash tool, and safety controls — is implemented from scratch in Python.

## How It Works

The agent operates in a continuous loop following the ReAct pattern:

```
You give a task
      │
      ▼
Model reasons → "I need to run ls"
      │
      ▼
Parser reads the response → extracts "ls"
      │
      ▼
Bash tool asks y/n → runs the command
      │
      ▼
Observation sent back to model
      │
      ▼
Model gives Final Answer → loop stops
```

The model always responds in this format, as instructed by the system prompt:

```
Thought: reasoning about what to do
Action: bash
Action Input: the command to run

— or when done —

Final Answer: the answer to the user
```

## Project Structure

```
├── agent.py
├── requirements.txt
├── .env               
├── .gitignore
└── config/
    └── system_prompt.md
```

## Requirements

- Python 3.10 or higher
- OpenAI API key (platform.openai.com)


## Configuration

Create a `.env` file in the project root:

```env
BASE_URL=https://api.openai.com/v1
MODEL=gpt-4o
API_KEY=your-openai-api-key-here
```

The agent's behavior is defined in `config/system_prompt.md`. This instructs the model to follow the ReAct format, only handle software engineering tasks, and decline unrelated topics.

## Usage

```bash
python3 agent.py
```

The agent will prompt `You:` and wait for input. Give it a software engineering task, for example:

```
List all files in the current directory
Create a file called hello.py with a hello world function
Show me the contents of agent.py
```

Each bash command requires manual approval (`y/n`) before it is executed.

## Security

- Every bash command requires explicit user approval before execution
- The agent is limited to a maximum of 10 iterations per session to prevent infinite loops
- The `.env` file is excluded from version control via `.gitignore`
- It is recommended to run the agent in a Docker container or isolated environment for full safety

## Constraints

- Built entirely in Python with direct calls to the OpenAI API
- No built-in function-calling — the model outputs raw text and a custom parser extracts actions
- No agent frameworks (LangChain, LangGraph, etc.)
- All core logic — loop, parser, bash tool — written from scratch
