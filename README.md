# terminal_companion
That's a simple python app for communication with the ChatGPT API provided by OpenAI directly from terminal.

To use it you simply need to get API key ferstly
Then add API key to environment variable
- for Windows  
  open CMD terminal and run  
  ```cmd
  setx OPENAI_API_KEY "your_API_key"
  ```
  to verify that all is good restart CMD terminal or open new one and run  
  ```cmd
  echo %OPENAI_API_KEY%
  ```
- for Linux/Mac  
  for zsh:  
  ```zsh
  echo "export OPENAI_API_KEY='your_API_key'" >> ~/.zshrc
  ```
  for bash:
  ```bash
  echo "export OPENAI_API_KEY='your_API_key'" >> ~/.bashrc
  ```
  to verify that all is good restart terminal or run   
  for zsh  
  ```zsh
  source ~/.zshrc
  ```
  for bash  
  ```bash
  source ~/.bashrc
  ```
  and then
  ```zsh
  echo $OPENAI_API_KEY
  ```

  
