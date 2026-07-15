# Load env variables and create client
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5"

# Helper functions
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text
import json


def generate_dataset():
    prompt = """
Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
    {
        "task": "Description of task",
    },
    ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""
  messages = []
  add_user_message(messages, prompt)
  add_assistant_message(messages, "```json")
  text = chat(messages, stop_sequences=["```"])
  return json.loads(text)

dataset = generate_dataset()
with open("dataset.json", "w") as f:
  json.dump(dataset, f, indent=2)

# model grading
def grade_by_model(test_case, output):
    # Create evaluation prompt
    eval_prompt = """
    You are an expert code reviewer. Evaluate this AI-generated solution.
    
    Original Task: 
    <task>
    {test_case["task"]}
    </task>
    
    Solution to Evaluate: 
    <solution>
    {output}
    </solution>

    Output Format
    Provide your evaluation as a structured JSON object with:
    - "strengths": An array of 1-3 key strengths
    - "weaknesses": An array of 1-3 key areas for improvement  
    - "reasoning": A concise explanation of your assessment
    - "score": A number between 1-10

    Respond with JSON. Keep your response concise and direct.
    Example response shape:
    {{
      "strengths": string[],
      "weaknesses": string[],
      "reasoning": string,
      "score": number
    }}
    """
    
    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")
    
    eval_text = chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)


# Running eval
def run_prompt(test_case):
  """Merges the prompt and test case input, then returns the result"""
  prompt = f"""
Please solve the following task:
{test_case["task"]}
"""
  messages = []
  add_user_message(messages, prompt)
  output = chat(messages)
  return output

def run_test_case(test_case):
  """Calls run_prompt, then grades the result"""
  output = run_prompt(test_case)
  # TODO - Grading
  model_grade = grade_by_model(test_case, output)
  score = model_grade["score"]
  reasoning = model_grade["reasoning"]
  
  return {
    "output": output,
    "test_case": test_case,
    "score": score,
    "reasoning": reasoning
    }

def run_eval(dataset):
  """Loads the dataset and calls run_test_case with each case"""
   results = []  
   for test_case in dataset:
      result = run_test_case(test_case)
      results.append(result)
   
   average_score = mean([result["score"] for result in results])
   print(f"Average score: {average_score}")

   return results

with open("dataset.json", "r") as f:
  dataset = json.load(f)

results = run_eval(dataset)

print(json.dumps(results, indent=2))

'''
Each result contains three key pieces of information:
output: The complete response from Claude
test_case: The original test case that was processed
score: The evaluation score (currently hardcoded)
'''
