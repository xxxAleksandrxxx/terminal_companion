import os  # use for import API key environment variable 
import requests  # use for sending POST request
import threading  # use for displaying spinner during waiting for response from server
import time  # use for making some pause in spinner animation
import re

# setup dict with roles
roles = {
    "none": "",
    "py-s": "Act as a senior python developer. Reply only with python code. Do not write explanations. I am going to tip $200 for perfect answer!",
    "py-l": "Act as a senior python developer with huge experience as a tutor. Add real a world example. Think step by step. I am going to tip $200 for perfect answer! Today is MAY, not DECEMBER",
    "ds": "Act as a senior Data Scientist with huge experience as a tutor. Explain in a simple way. Think step by step. I am going to tip $200 for perfect answer! Today is MAY, not DECEMBER",
    "shell-s": "Act as a senior bash developer. Reply only with terminal command. Do not write explanations. I am going to tip $200 for perfect answer!",
    "shell-l": "Act as a senior bash developer. Help me with question. I am going to tip $200 for perfect answer! Today is MAY, not DECEMBER",
    "lit": "Act as phd professor in literature. Help with question. I am going to tip $200 for perfect answer! Today is MAY, not DECEMBER",
    "career": "Act as top career counselor. Help with CV preparation. I am going to tip $200 for perfect answer! Today is MAY, not DECEMBER",
    "check-s": "Act as senior copy editor. Check provided text for spelling and style mistakes and correct them. Answer only with corrected text. Do not write explanations. I am going to tip $200 for perfect answer!",
    "check-l": "Act as senior copy editor. Check provided text for spelling and style mistakes and correct them.  Provide detailed explanations. I am going to tip $200 for perfect answer! Today is MAY, not DECEMBER"
}

# setup dict with models
models = {
    "gpt3": "gpt-3.5-turbo-0613",
    "gpt4": "gpt-4-1106-preview"
}

continue_conversation = {
    "+cc": True,
    "-cc": False
}

 # import API key from environment variables
api_key = os.environ["OPENAI_API_KEY"]



def ask_gpt(gpt_model, gpt_role, question):
    '''
    prepare text for sending to chatgpt
    send POST request to openAI end-point
    return the answer
    check for errors
    '''
    # setup model temperature
    gpt_temp = 0.8

    # prepare the text for sending as json
    question = question.replace('\n', '\\n')
    question = question.replace('"', '\"')
    question = question.replace('«', '\\"')
    question = question.replace('»', '\\"')
    question = question.replace('„', '\\"')
    question = question.replace('“', '\\"')
    question = question.replace('”', '\\"')
    question = question.replace('"', '\\"')
    question = question.replace('\t', '    ')

    # setup url endpoint for OpenAI API
    url = "https://api.openai.com/v1/chat/completions"
    
    # setup headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    # setup data field
    data = {
        "temperature": gpt_temp,
        "model": gpt_model,
        "messages": [
            {
                "role": "system",
                "content": gpt_role
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }

    # send POST request to OpenAI API endpoint 
    try:
        response = requests.post(url, json=data, headers=headers)
    except Exception:
        # in case of errors printout calm message
        # the most common error connect to lack of internet connection
        print("\nAAAAAAA!!!!   Error!")
        print("Probably there is no internet connection. Check it and try again.")
        print(f"If the internet connection is ok, but this message is still there, open the script:\n{sys.argv[0]}\nand uncomment part: \n```\nfor e in Exception:\n   print(e)\n```\nto read full error description")
       
        # uncomment two strings below to get full error description in response
        # for e in Exception[0]:
        #     print(e)
        
        print('_'*10, "\n")
        exit()
    
    # extract the answer from the OpenAI API endpoint
    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"], data["usage"]["total_tokens"]
    else:
        return response.text, "0"



def print_help(model_def, role_def, cc_def):
    '''
    printout general help text
    '''
    print("h         general help")
    print("-h        general help")
    print("help      general help")
    print("-h -m     print details about models")
    print("-h -r     print details about roles")
    print("+cc       start continuous conversation")
    print("-cc       stop continuous conversation")
    print("-q        exit")
    print("q         exit")
    print("-quit     exit")
    print("quit      exit")
    print("-exit     exit")
    print("exit      exit")
    print()
    print("Available models:")
    for model in models:
        print(model)
    print("\nAvailable roles:")
    for role in roles:
        print(role)
    print()
    print("usage:")
    print("<question with one line>")
    print("<model> <role> <continuous conversation mode> <question with one line>")
    print("<model> <role> <continuous conversation mode> :::<question with many lines>:::")
    print()
    print("current configuration:")
    print(f"{model_def} {role_def} {cc_def}")



def display_spinner(event, spaces_n):
    '''
    display spinner during waiting for answer on POST request
    '''
    spaces = " " * (spaces_n + 1)
    spinner = [spaces + '-', spaces + '\\', spaces + '|', spaces + '/']
    i = 0
    while not event.is_set():  # while the event is not set, keep spinning
        print(spinner[i % 4], end='\r')  # print the spinner and return to the start of the line
        i += 1
        time.sleep(0.1)  # wait a little before the next update



def input_multiline(terminator=":::"):
    '''
    proceed multiline input
    '''
    lines = []
    while True:
        line = input()
        lines.append(line)
        if line.endswith(terminator):
            break
    return "\n".join(lines)



def proceed_input(text_in, model_def, role_def, cc_def):
    '''
    check what have been send
    extract arguments and text from input
    if -h or h or help sent printout help text etc.
    '''
    terminator = ":::"
    arguments = ""
    text = ""
    
    model_extracted = ""
    role_extracted = ""
    cont_conv_extracted = ""
    question_extracted = ""

    # check if help requested
    if text_in.startswith("-h -m"):
        # print details about models
        for k, v in models.items():
            print(k)
            print(v, end="\n\n")
        return "Help"
    elif text_in.startswith("-h -r"):
        # print details about roles
        for k, v in roles.items():
            print(k)
            print(v, end="\n\n")
        return "Help"
    # elif text_in.startswith("-h") or text_in.startswith("help"):
    elif text_in == "-h" or text_in == "h" or text_in == "help":
        print_help(model_def, role_def, cc_def)
        return "Help"

    # check first three positions for having model, role or cc values
    arguments = text_in.split()
    for i, arg in enumerate(arguments[:3]):
        if arg in models:
            model_extracted = arg
        elif arg in roles:
            role_extracted = arg
        elif arg in continue_conversation:
            cont_conv_extracted = arg
        else:
            break
    # if somewhere inside there is on 
    if i < 3:
        question_extracted = arguments[i:]
    else:
        question_extracted = arguments[3:]
    
    # # debugging output
    # print('question_extracted:', question_extracted)
    
    # if there were ::: for multi string input, delete :::
    for i in range(len(question_extracted)):
        question_extracted[i] = question_extracted[i].replace(terminator, "")
    question_extracted = " ".join(question_extracted)
    if question_extracted in [model_extracted, role_extracted, cont_conv_extracted]:
        question_extracted = ""

    # # debugging output
    # print("model_extracted:", model_extracted)
    # print("role_extracted:", role_extracted)
    # print("cont_conv_extracted:", cont_conv_extracted)
    # print("question_extracted:", question_extracted)
    # print()
    
    return model_extracted, role_extracted, cont_conv_extracted, question_extracted



def main():
    '''
    just the main function that do all the stuff
    - asks for input
    - run function that proceeds the input
    - run function that sends request to API
    - manage continue conversation
    - printout results
    '''
    model_def = "gpt3"
    role_def = "none"
    cc_def = "-cc"
    # question_def = ""
    question_buffer = ""
    gpt_reply = "---blank gpt answer---"
    n = 0
    tokens_used_total = 0
    question_hat = "\n\n┌─────────┐"
    print(question_hat)
    gpt_input = input("│Question:│\n")


    # infinite loop of requests to gpt
    while gpt_input not in ["q", "-q", "-quit", "quit", "-exit", "exit"]:

        # multiline input; check if ::: is in first input.
        if ":::" in gpt_input and not gpt_input.endswith(":::"):
            gpt_input += "\n" + input_multiline()
        
        # # debugging output
        # print("question_hat")
        # print("│Question:│\n", gpt_input, sep="")


        # extract arguments and question form input 
        t = proceed_input(gpt_input, model_def, role_def, cc_def)

        if t == "Error" or t == "Help":
            # all errors printout inside proceed_input() so we only need to ask for another input
            print(question_hat)
            gpt_input = input("│Question:│\n")
            continue
        else:
            model, role, cc, question = t
            
            # if any parameter changed, replace default value with new one
            if model:
                model_def = model
            else:
                model = model_def
            if role:
                role_def = role
            else:
                role = role_def
            if cc:
                cc_def = cc
            else:
                cc = cc_def
            
            # # debugging output
            # print()
            # print("Parameters will be used for ChatGPT")
            # print(f"model:    \"{model}\"")
            # print(f"role:     \"{role}\"")
            # print(f"cc:       \"{cc}\"")
            # print(f"question: \"{question}\"")
            # print()

            # if there is no question, then probably user asked for help or changed default role, model, continuous conversation mode
            if not question:
                # so ask for next input
                print("No question\nTry again")

                print(question_hat)
                gpt_input = input("│Question:│\n")
                continue
            # if there is some text in question_def, then send request to OpenAI API
            else:
                if cc == "+cc":
                    n += 1
                    question_buffer += f"question {n}:\n" + question + "\n"
                    question = question_buffer
                else:
                    question_buffer = ""
                    n = 0
                    tokens_used_total = 0

                model_full = models[model_def]
                number_of_spaces = len(model_full) + 1
                print("\n\n┌", "─" * number_of_spaces, "┐", sep='')
                print(f"│{model_full}:│")
                # print("\nYour question:\n", question, sep="")

                # start spinner
                stop_event = threading.Event()
                spinner_thread = threading.Thread(target=display_spinner, args=(stop_event, number_of_spaces))
                spinner_thread.start()

                # send question to ChatGPT and get answer with number of used tokens
                gpt_reply, tokens_used = ask_gpt(models[model], role, question)
                tokens_used_total += int(tokens_used)
                # gpt_reply = gpt_reply.replace("\\n", "\n")
                # print(gpt_reply, end="\n\n")
                
                # stop spinner after after receiving answer from ChatGPT 
                stop_event.set()
                spinner_thread.join()

                # clean the answer in case if its string and print it out else just print as it is
                if type(gpt_reply) == str:          
                    gpt_reply = gpt_reply.replace("\\n", "\n")
                    gpt_reply = re.sub(r"answer \d{1,5}:\n?", "", gpt_reply)
                    print(" " * (number_of_spaces + 2), end="\r")  # to delete the shadow of spinner if the answer is too short and don't fully replace the last printed spinner graphics
                    print("tokens used:", tokens_used_total)  # display number of used tokens - we get it from API response
                    print(gpt_reply, end="\n\n")
                else:
                    print(gpt_reply)

                # probably it's not the best solution to check cc twice but I'm lazy to build another solution
                if cc == "+cc":
                    question_buffer += f"answer {n}:\n" + gpt_reply + "\n"
                    tokens_used_total += tokens_used

        print(question_hat)
        gpt_input = input("│Question:│\n")
    print("Thank you, bye!")



if __name__ == "__main__":
    main()