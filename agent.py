import os
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
)

def parse_response(response_text):
    if "Final Answer:" in response_text:
        return "final", response_text.split("Final Answer:")[-1].strip()
    
    if "Action:" in response_text and "Action Input:" in response_text:
        action = response_text.split("Action:")[-1].split("\n")[0].strip()
        action_input = response_text.split("Action Input:")[-1].strip()
        return "action", (action, action_input)
    
    return "unknown", response_text

def run_bash(command):
    print(f"\nAgent wants to run: {command}")
    confirm = input("Allow? (y/n): ")
    
    if confirm.lower() != "y":
        return "Command was rejected by user."
    
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout or result.stderr

with open("config/system_prompt.md", "r") as f:
    system_prompt = f.read()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": input("You: ")}
]

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
)

for _ in range(10):
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
    )
    
    reply = response.choices[0].message.content
    print(f"\nAgent: {reply}")
    
    action_type, value = parse_response(reply)
    
    if action_type == "final":
        break
    
    if action_type == "action":
        tool, command = value
        observation = run_bash(command)
        print(f"\nObservation: {observation}")
        
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"Observation: {observation}"})