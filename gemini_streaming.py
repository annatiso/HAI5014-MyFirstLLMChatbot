import os
from openai import OpenAI

token = os.environ["GOOGLE_API_KEY"]
endpoint = "https://generativelanguage.googleapis.com/v1beta/openai/"
model_name = "gemini-2.0-flash"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def get_response(user_input, messages=None):
what    if messages is None:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            }
        ]
    
    # Add the user's input to the conversation history
    messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Use the full conversation history for context
    response = client.chat.completions.create(
        messages=messages,  # Pass the entire conversation history
        model=model_name,
        stream=True,
        stream_options={'include_usage': True}
    )
    
    print("\nAssistant: ", end="")
    assistant_response = ""
    usage = None
    for update in response:
        if update.choices and update.choices[0].delta:
            content = update.choices[0].delta.content or ""
            print(content, end="")
            assistant_response += content
        if update.usage:
            usage = update.usage
    
    # Add the assistant's response to the conversation history
    messages.append({
        "role": "assistant",
        "content": assistant_response
    })
    
    if usage:
        print("\n")
        for k, v in usage.dict().items():
            print(f"{k} = {v}")
    
    return messages

def main():
    print("Welcome to the interactive Gemini chat! (Type 'exit' to quit)")
    conversation_history = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        }
    ]
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        conversation_history = get_response(user_input, conversation_history)

if __name__ == "__main__":
    main()