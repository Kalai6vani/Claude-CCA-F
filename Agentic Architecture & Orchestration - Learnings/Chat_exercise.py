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

#-------------------------main-------------------------------
messages = []

#Use a 'while True' loop to run the chatbot forever
while True:
  #Get user input
  user_input = input("> ")
  print(">", user_input)

  #Add user input to the list of messages
  add_user_message(messages, user_input)
  #Call Claude with the 'chat' function
  answer = chat(messages)
  #Add generated text to the list of messages
  add_assistant_message(messages, answer)
  #Print the generated text
  print("---")
  print(answer)
  print("---")
