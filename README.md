# AI Todo List Agent with CrewAI

An intelligent AI-powered Todo List Assistant that helps manage your tasks through natural language conversation. Built with Python using CrewAI framework for advanced agent capabilities.

## Features

- Natural language task management powered by CrewAI agents
- Create new todos with intelligent task understanding
- List all todos with formatted output
- Search todos with semantic understanding
- Delete todos by ID
- Conversational interface with friendly responses
- Built-in error handling and response formatting
- Tool-based architecture for extensibility

## Prerequisites

- Python 3.8+
- PostgreSQL database
- CrewAI and its dependencies

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
```

## Database Setup

The application uses PostgreSQL as its database. The tables will be automatically created when you first run the application, as defined in the models.py file.

## Architecture

The application uses CrewAI's agent-based architecture:

1. **Tools**: Custom tools defined in `tools.py` using CrewAI's `@tool` decorator
   - GetAllTodos: Retrieve all todos
   - CreateTodo: Add new todos
   - DeleteTodoById: Remove todos
   - SearchTodo: Find specific todos

2. **Agent**: A single Todo List Assistant agent that:
   - Understands natural language requests
   - Uses appropriate tools based on context
   - Provides friendly and helpful responses
   - Maintains conversation context

3. **Task Processing**: Each user request is processed as a task with:
   - Clear input description
   - Expected output format
   - Proper error handling
   - Consistent response structure

## Usage

**1. Start the assistant**:
```sh
python todo_crew.py
```

**2. Interact with the assistant using natural language commands**:
- "Add buy groceries to my list"
- "Show me all my todos"
- "Search for grocery related tasks"
- "Delete todo number 5"
- Type "exit" or "quit" to end the session

## Response Format

The assistant provides responses that:
1. Acknowledge the user's request
2. Show the result of the action taken
3. Provide a helpful follow-up question or suggestion
4. Use emojis appropriately to maintain a friendly tone
5. Keep the response concise and to the point

## Extending the Agent

The agent can be extended by:
1. Adding new tools in `tools.py` using the `@tool` decorator
2. Modifying the agent's backstory and goals
3. Adding new task types and processing logic
4. Implementing additional CrewAI features like planning and delegation

## Contributing

Feel free to submit issues and enhancement requests!
