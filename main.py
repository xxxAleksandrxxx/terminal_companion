import os  # use for import API key environment variable 
import requests  # use for sending POST request
import threading  # use for displaying spinner during waiting for response from server
import time  # use for making some pause in spinner animation
import re
import readline  # for right and left keys movements across the input and for input history feature 
from MODELS import models  # import models from MODELS.py file
from ROLES import roles  # import roles from ROLES.py file



# possible values for continue conversation
continue_conversation = {
    "+cc": True,  # continue conversation mode on
    "-cc": False  # continue conversation mode off
}

 # import API key from environment variables
api_key = os.environ["OPENAI_API_KEY"]

# setup temperature for ChatGPT; link for reference: https://platform.openai.com/docs/guides/text-generation/faq
gpt_temp = 0.8  # using as global parameter probably not the best idea but let it be so for a while



def ask_gpt(gpt_model, gpt_role, question, stop_event):
    '''
    prepare text for sending to chatgpt
    send POST request to openAI end-point
    return the answer
    check for errors

    stop_event - to stop spinner thread
    '''

    # prepare the text for sending as json
    question = question.replace('\n', '\\n')
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
                "content": roles[gpt_role]
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
    except Exception as e:
        # in case of errors printout calm message
        # the most common error connect to lack of internet connection
        print("\nAAAAAAA!!!!   Error!")
        # print("\nAAAAAAA!!!!   Error!\n", e, "\n")
        print("Most likely that there is no internet connection. Check it firstly")
        print('_'*10, "\n")
        
        stop_event.set()  # for spinner handling
        raise  #  reraise exception to be handled by caller

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
    print("<enter>   check current settings")
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
    print(":::<question\nwith\nmany\nlines>:::")
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
    # text = ""  # probably not used 
    
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
    # print current status on ?
    elif text_in == "?":
        print(f"{model_def} {role_def} {cc_def}")
        return "Help"

    # check first three positions if there is model, role or cc value
    arguments = text_in.split()
    i = 0

    # looking if there is model, role or conversation mode in the input; they have to be first three words in this case
    for arg in arguments[:3]:
        if arg in models:
            model_extracted = arg
        elif arg in roles:
            role_extracted = arg
        elif arg in continue_conversation:
            cont_conv_extracted = arg
        else:
            break
        i += 1
    # if there were less then 3 words we extract the question after the last one or if all 3 exist we extract the text after all them as question 
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
    role_def = list(roles.keys())[0]  # assign first key from roles as a default role. it assume to be something relating to empty or neutral value
    cc_def = "-cc"
    question_buffer = ""
    gpt_reply = "---blank gpt answer---"
    n = 0
    tokens_used_total = 0
    
    question_hat = "\n\n┌─────────┐\n│Question:│"  # setup how we mark user input
    print(question_hat)
    gpt_input = input()  # initial input

    # infinite loop of requests to gpt
    while gpt_input not in ["q", "-q", "-quit", "quit", "-exit", "exit"]:

        # check if ::: is in first input for activating multiline input
        if ":::" in gpt_input and not gpt_input.endswith(":::"):
            gpt_input += "\n" + input_multiline()

        # extract arguments (model, role, conversation mode) and question form provided input 
        t = proceed_input(gpt_input, model_def, role_def, cc_def)

        if t == "Error" or t == "Help":
            # all errors printout inside proceed_input() so we only need to ask for another input
            print(question_hat)
            # gpt_input = input("│Question:│\n")
            gpt_input = input()
            continue
        else:
            # if all is ok, proceed_input return model, role, cc and question
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
                # print current settings
                print("Current settings:")
                print(f"{model} {role} {cc}")
                # ask for next input
                print(question_hat)
                gpt_input = input()
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

                # For handling possible errors during request to the server
                stop_event = threading.Event()
                spinner_thread = threading.Thread(target=display_spinner, args=(stop_event, number_of_spaces))
                try:
                # start spinner
                    spinner_thread.start()
                    
                    # send question to ChatGPT and get answer with number of used tokens
                    gpt_reply, tokens_used = ask_gpt(models[model], role, question, stop_event)  # extract ChatGPT reply and number of total tokens used by OpenAI to send and answer the question 
                    tokens_used_total += int(tokens_used)  # summarize tokens in case of conversation mode on 

                    # stop spinner after receiving answer from ChatGPT 
                    stop_event.set()
                    spinner_thread.join()
                    if type(gpt_reply) == str:          
                        gpt_reply = gpt_reply.replace("\\n", "\n")
                        gpt_reply = re.sub(r"answer \d{1,5}:\n?", "", gpt_reply)
                        print(" " * (number_of_spaces + 2), end="\r")  # to delete the shadow of spinner if the answer is too short and don't fully replace the last printed spinner graphics
                        print("tokens used:", tokens_used_total)  # display number of used tokens, extracted from API response and summarized in case of conversation mode on
                        print(gpt_reply, end="\n\n")
                    else:
                        print(gpt_reply)

                # probably it's not the best solution to check cc twice but I'm lazy to build another solution
                    if cc == "+cc":
                        question_buffer += f"answer {n}:\n" + gpt_reply + "\n"
                        tokens_used_total += tokens_used
                except Exception as e:
                    # if some error happened during spinner rotation, stop spinner and printout the error
                    stop_event.set()
                    spinner_thread.join()
                    print("Error: Spinner exception happened!")
                    print(e)
                   
        print(question_hat)
        gpt_input = input()
    print("Thank you, bye!\n\n")



if __name__ == "__main__":
    main()