import asyncio
import json
from tools import tools
import replicate
from typing import Dict, Any, List

SYSTEM_PROMPT = """
You are a To-Do List Assistant. Your primary goal is to help users manage their tasks effectively.

*Guidelines*:
- Keep responses as valid JSON
- Always verify actions before executing
- If you cannot understand the user's request, ask for clarification.
- Avoid inserting same task multiple times.
- Avoid repeating the plan response multiple times. After planning, proceed to the next step.
- End with friendly output including task status and follow-up

*Available Tools For You*:
- getAllTodos(): Returns all user's Tasks/Todos from database
- createTodo(todo: string): Creates a new task/todo in the DB and returns the ID
- deleteTodoById(id: string): Deletes the task/todo by ID
- searchTodo(query: string): Searches tasks/todos matching the query string

*RESPONSE FORMAT*:
You must ALWAYS follow this process for EVERY user message and must ALWAYS respond with ONE of these JSON formats

1. {"type": "plan", "plan": "description of what you'll do"}
2. {"type": "action", "function": "toolName", "input": "parameter"}
3. {"type": "observation", "observation": "observation from the action"}
4. {"type": "output", "output": "message to user"}

*Example*:
User: "Buy groceries tomorrow"
{"type": "plan", "plan": "Creating new todo"}
{"type": "action", "function": "createTodo", "input": "Buy groceries tomorrow"}
{"type": "observation", "observation": "2"}
{"type": "output", "output": "Added to your tasks. Need anything else?"}

User: "what do I need to do?"
{"type": "plan", "plan": "I will check all current todos"}
{"type": "action", "function": "getAllTodos", "input": ""}
{"type": "observation", "observation": "[list of todos]"}
{"type": "output", "output": "Here are your current tasks: [list todos]. Would you like to add a new task?"}
"""


def format_conversation(messages: List[dict]) -> str:
    conversation = ""
    for message in messages:
        content = message["content"]
        if message["role"] == "user":
            try:
                user_msg = json.loads(content)
                conversation += f'User: {user_msg["user"]}\n'
            except:
                conversation += f"User: {content}\n"
        elif message["role"] == "assistant":
            conversation += f"Assistant: {content}\n"
        elif message["role"] == "developer":
            try:
                obs_msg = json.loads(content)
                conversation += f'Observation: {json.dumps(obs_msg["observation"])}\n'
            except:
                conversation += f"Observation: {content}\n"
    return conversation


def extract_json_from_response(response_text: str) -> dict:
    """Extract the first valid JSON object from the response."""
    try:
        # Find the first occurrence of '{' and the matching '}'
        start = response_text.find("{")
        if start == -1:
            return None

        stack = []
        for i in range(start, len(response_text)):
            if response_text[i] == "{":
                stack.append(i)
            elif response_text[i] == "}":
                if stack:
                    stack.pop()
                    if not stack:
                        end = i + 1
                        json_str = response_text[start:end]
                        return json.loads(json_str)

        return None
    except Exception as e:
        return None


async def main():
    messages = []
    last_action_type = None

    while True:
        try:
            query = input("😁: ")
            if query.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            user_message = {"type": "user", "user": query}
            messages.append({"role": "user", "content": json.dumps(user_message)})

            while True:
                try:
                    conversation = format_conversation(messages)
                    # print(f"Conversation: {conversation}")

                    # Call Replicate API
                    output = await replicate.async_run(
                        "meta/meta-llama-3-8b-instruct",
                        input={
                            "prompt": conversation,
                            "system_prompt": SYSTEM_PROMPT,
                            "temperature": 0.2,
                            "max_tokens": 500,
                            "top_p": 0.95,
                            "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
                        },
                    )

                    response_text = "".join(output).strip()

                    # Extract and parse the first valid JSON object
                    try:
                        action = extract_json_from_response(response_text)
                        if action is None:
                            print(
                                "Warning: No valid JSON found in response. Retrying..."
                            )
                            continue
                        messages.append(
                            {"role": "assistant", "content": json.dumps(action)}
                        )

                        if action["type"] == "output":
                            print(f"🤖: {action['output']}")
                            break
                        elif action["type"] == "action":
                            fn = tools.get(action["function"])
                            if not fn:
                                print(f"Error: Invalid tool call: {action['function']}")
                                break

                            try:
                                observation = fn(action.get("input", None))
                                observation_message = {
                                    "type": "observation",
                                    "observation": observation,
                                }
                                messages.append(
                                    {
                                        "role": "developer",
                                        "content": json.dumps(observation_message),
                                    }
                                )
                                last_action_type = "action"
                            except Exception as e:
                                print(f"Tool execution error: {str(e)}")
                                break
                        elif action["type"] == "plan":
                            if last_action_type == "plan":
                                continue
                            last_action_type = "plan"
                        elif action["type"] == "observation":
                            if last_action_type != "action":
                                continue
                        else:
                            print(f"Unknown action type: {action['type']}")
                            break

                    except json.JSONDecodeError as e:
                        print(f"JSON parsing error: {str(e)}")
                        print("Response was:", response_text)
                        break
                    except ValueError as e:
                        print(f"Error: {str(e)}")
                        break

                except Exception as e:
                    print(f"Error during processing: {str(e)}")
                    break

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
