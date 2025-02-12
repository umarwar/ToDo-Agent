# AI Todo List Agent

An intelligent AI-powered Todo List Assistant that helps manage your tasks through natural language conversation. Built with Python using Meta's Llama 3 model via Replicate.

## Features

- Natural language task management
- Create new todos
- List all todos
- Search todos
- Delete todos by ID
- Conversational interface

## Prerequisites

- Python 3.8+
- PostgreSQL database
- Replicate API key

## Installation

1. Clone the repository:
```sh
git clone <repository-url>
cd ToDo-Agent
```

2. Create and activate a virtual environment:
```sh
python -m venv venv

source venv/bin/activate  #Mac/linux
venv\Scripts\activate  #Windows
```


3. Install dependencies:
```sh
pip install -r requirements.txt
```


4. Create a `.env` file in the root directory with the following variables:
```sh
DATABASE_URL=postgresql://username:password@host:port/database
REPLICATE_API_TOKEN=your_replicate_api_token
```

## Database Setup

The application uses PostgreSQL as its database. The tables will be automatically created when you first run the application, as defined in the models.py file (see lines 14-19).

## Usage

**1. Start the assistant**:
```sh
python agent.py
```

**2. Interact with the assistant using natural language commands**:
- "Add buy groceries to my list"
- "Show me all my todos"
- "Search for grocery related tasks"
- "Delete todo number 5"
- Type "exit" or "quit" to end the session

The assistant follows a structured conversation flow:
1. **Plan**: Determines the appropriate action based on user input
2. **Action**: Executes the required tool (getAllTodos, createTodo, etc.)
3. **Observation**: Processes the result of the action
4. **Output**: Provides a friendly response to the user