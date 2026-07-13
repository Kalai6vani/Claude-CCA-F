#Helper functions to maintain MULTI - TURN CONVERSATION
def add_user_message(messages, text):
  user_message = {"role": "user", "content": text}
  messages.append(user_message)

def add_assistant_message(messages, text):
  assistant_message = {"role": "assistant", "content": text}
  messages.append(assistant_message)

def chat(messages):
  message = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
  )
  return message.content[0].text

#------------------------------------main-------------------------------------
messages = []

add_user_message(messages, "Generate a very short event bridge rule as json")
add_assistant_message(messages, "```json")

text = chat(messages, stop_sequences=["```"])
text

#import json
#json.load(text.strip())
