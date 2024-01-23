# terminal_companion
# Description
That's a simple python app for communication with the ChatGPT API provided by OpenAI directly from terminal.  

**Pros:**  
- different models (gpt-3.5-turbo-0613 and gpt-4-1106-preview up to Jan 2024)
- custom roles
- continue conversation with seamless switching between models and roles
- switch model, role, continue conversation mode on the fly
- simple one-line requests
- complex multi-line requests
- use only requests library
- use API key stored in your environment variables for safety
- it has spinner to show that we are waiting for server response and the app hasn't frozen yet 😅
- it has even help feature! 😁  

**Cons:**
- All the logic, models and roles are stored in main.py file. Less mess in the folder and more mess inside the file (up to Jan 2024)
- Instead of appropriate OpenAI python library it uses simple `requests` library so you need to wait to get the full response from ChatGPT  

**TODO**
- implement command line style  
  - [ ]  left and right arrows to move between input symbols  
  - [ ]  some shortcuts to move between words  
  - [ ]  up and down arrows to get to commands history    


# Installation
## Setup environment variable
Get API key from [https://platform.openai.com/](https://platform.openai.com/) firstly.  
Then add API key to environment variable
- **for Windows**  
  open CMD terminal and run  
  ```cmd
  set OPENAI_API_KEY "your_API_key"
  ```
  to verify that all is good restart CMD terminal or open new one and run  
  ```cmd
  echo %OPENAI_API_KEY%
  ```
- **for Linux/Mac**  
  for zsh:  
  ```zsh
  echo "export OPENAI_API_KEY='your_API_key'" >> ~/.zshrc
  source ~/.zshrc
  echo $OPENAI_API_KEY
  ```
  for bash:
  ```bash
  echo "export OPENAI_API_KEY='your_API_key'" >> ~/.bashrc
  source ~/.bashrc
  echo $OPENAI_API_KEY
  ```

## Copy the project
Copy the project to your desired folder. For example to Desktop and using ssh
```zsh
cd ~/Desktop
git clone git@github.com:xxxAleksandrxxx/terminal_companion.git
cd terminal_companion
```

  ## Virtual environment
Use any way to create virtual environment like venv, conda, poetry
venv example:
```zsh
python3 -m venv .venv
```

Activate it 
venv example:
```zsh
source source .venv/bin/activate 
```

Insatall requerements
```zsh
pip install -r requirements.txt
```

# Usage
Run the main.py file
```zsh
python3 main.py
```

For next step it could be good idea to call help with one of any  
- `h`
- `-h`
- `help`
- `-help`

Or simply write your question straightaway.  

To exit from the app:
- `q`
- `-q`
- `q`
- `-quit`
- `quit`
- `-exit`
- `exit` 


By default it starts with:  
```python
model: gpt3              # gpt-3.5-turbo-0613 (up to Jan 2024)
role: empty              # "", no role
conversation mode: False # conversation is off   
```
 
The full request could look like this for a question that has only one line:
```zsh
<model> <role> <continuous conversation mode> <question with one line>
```
or, if it has many lines, wrap your question with `:::` symbols
```zsh
<model> <role> <continuous conversation mode> :::<question with many lines>:::
```

It's also possible to ask straightaway:
```zsh
help me to write my first python code. it should be something really interesting!
```


## Models (valid up to Jan 2024):
```python
"gpt3": "gpt-3.5-turbo-0613",
"gpt4": "gpt-4-1106-preview"
```

## Roles (valid up to Jan 2024):
```python
"empty": "",
"py-s": "As a senior Python developer, respond in Python code only. Your solution could earn a $200 tip.",
"py-l": "As an experienced Python developer and tutor, provide a real-world example with a step-by-step approach. A $200 tip is possible for excellence. It's May, not December.",
"ds": "As a senior Data Scientist and tutor, explain simply and step-by-step. A $200 tip awaits the perfect answer. It's May, not December.",
"shell-s": "As a senior bash developer, respond with terminal commands only. A perfect answer may receive a $200 tip.",
"shell-l": "As a senior bash developer, assist with my question. A $200 tip is offered for the perfect answer. It's May, not December.",
"lit": "As a PhD professor in literature, assist with my question. A perfect answer could earn a $200 tip. It's May, not December.",
"career": "As a top career counselor, aid with CV preparation. There's a $200 tip for the perfect answer. It's May, not December.",
"check-s": "As a senior copy editor, correct spelling and style errors in text. Respond with only the corrected text. A $200 tip is possible for perfection. Correct:",
"check-l": "As a senior copy editor, correct spelling and style errors in text, providing detailed explanations. A $200 tip for excellence. It's May, not December. Text:"
```

## Conversation mode
```python
"+cc": True,
"-cc": False
```


# Some examples:

To change the model simply write   
```zsh
gpt4
```

or change the role and add any question  
```zsh
gpt4 hi! help me to write my first python code. it should be something really interesting!
```

Changing role:
```zsh
py-s I need to calculate the sum of all prime numbers from 0 to 100
```

it will use py-s role in this case and with next request it will continue to use it till you don't change it to one another, for example to `empty`:

```zsh
epmty tell me a joke
``` 


To start conversation simply start your question with `+cc`
```zsh
q:
+cc Hi! how are you?

a:
I'm an AI, so I don't have feelings, but I'm here to help you. How can I assist you today?

q:
what can you do?

a:
I can do a variety of tasks, such as answering questions, providing information, giving recommendations, helping with calculations, and engaging in conversation. Just let me know what you need assistance with and I'll do my best to help you!

q:
what was my first question?

a:
Your first question was "Hi! how are you?"
```
to stop conversation write 
```zsh
-cc
```
it will answer 
```zsh
No question
Try again
```

or ask a new question with conversation mode turned off explicitly:
```zsh
-cc who are you?
```