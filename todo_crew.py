from functools import lru_cache
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
from tools import getAllTodos, createTodo, deleteTodoById, searchTodo
from typing import List, Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@lru_cache(maxsize=1)
def initialize_llm():
    return LLM(
        # model="ollama/deepseek-r1:1.5b",
        # base_url="http://localhost:11434",
        model="gpt-4o",
        api_key=os.environ.get("OPENAPI_API_KEY"),
    )


llm = initialize_llm()

# Define the Todo Agent
todo_agent = Agent(
    role="Todo List Assistant",
    goal="Help users manage their tasks effectively through natural language interaction",
    backstory="""You are an intelligent Todo List Assistant that helps users manage their tasks.
    You can create new todos, list existing ones, search for specific tasks, and delete tasks when needed.
    You maintain a friendly and helpful demeanor while ensuring tasks are managed efficiently.
    Always provide clear and concise responses.""",
    tools=[getAllTodos, createTodo, deleteTodoById, searchTodo],
    llm=llm,
    verbose=False,
)


def process_user_input(user_input: str) -> str:
    """
    Process user input and return the appropriate response using CrewAI
    """
    # Create a task for the agent
    task = Task(
        description=f"Process the following user request: {user_input}",
        expected_output="""A clear and friendly response that:
        1. Acknowledges the user's request
        2. Shows the result of the action taken
        3. Provides a helpful follow-up question or suggestion
        4. Uses emojis appropriately to maintain a friendly tone
        5. Keeps the response concise and to the point""",
        agent=todo_agent,
    )

    # Create a crew with our agent
    crew = Crew(agents=[todo_agent], tasks=[task], verbose=False)

    # Execute the task
    result = crew.kickoff()
    return result


def main():
    print("🤖 Todo List Assistant (CrewAI Version)")
    print("Type 'exit' or 'quit' to end the session")

    while True:
        try:
            user_input = input("😁: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            response = process_user_input(user_input)
            print(f"🤖: {response}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
