#!/usr/bin/env python3
import argparse
import os
import platform
import sys
import json
import io
import importlib, inspect

from rich import pager
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

from resources import config
# from resources.conduit import get_completion
from resources.conduit import get_chat, get_models, get_image, get_variant, get_edit


console = Console()
version = "0.5.1"
_session_file_ = ".messages.json"

available_parameters = {}
available_descr = {}
available_functions = {}

def get_lindata():
    lindata = "Users Kernel:" + platform.platform() + "\n" \
              "Users OS:" + os.uname().version + "\n" \
              "Users Shell:" + os.environ.get("SHELL", "").split("/")[-1] + "\n\n"
    return lindata


def post_completion(openai_response):
    if config.get_expert_mode() != "true":
        openai_response += '\n\n[Notice] OpenAI\'s models have limited knowledge after 2020. Commands and versions' \
                           'may be outdated. Recommendations are not guaranteed to work and may be dangerous.' \
                           'To disable this notice, switch to expert mode with `oai --expert`.'
    return openai_response

def get_session():
    with open(_session_file_) as sf:
      messages=json.load(sf)
    return messages

def put_session(messages):
    try:
      to_unicode = unicode
    except NameError:
      to_unicode = str
    with open(_session_file_, 'w', encoding='utf8') as outfile:
      str_ = json.dumps(messages,
                       indent=4, sort_keys=True,
                       separators=(',', ': '), ensure_ascii=False)
      outfile.write(to_unicode(str_))

def read_text(url):
    messages = ""
    with open(url) as sf:
      for line in sf:
        line = line.rstrip()
        messages += line + ' '
    return messages

def stripp_it(rawt):
    rawt.replace('\n', ' ').replace('\r', '')
    rawt.replace('\t', ' ')
    return rawt

def read_csv(url):
    messages = ""
    with open(url) as sf:
      for line in sf:
        line = line.rstrip()
        messages += line + '\n'
    return messages
    

def read_pdf(prompt):
    console.log("PDF not supported yet")
    exit()

def extract_jsonstr(prompt):
    file, ext = prompt.split('.')
    if ext == 'txt':
      rawt = read_text(prompt)
      pro = stripp_it(rawt)
      
    elif ext in ['py', 'html', 'css', 'c', 'h', 'cpp', 'hpp']:
      rawt = read_text(prompt)
      pro = stripp_it(rawt)
      
    elif ext == 'csv':
      rawt = read_csv(prompt)
      pro = stripp_it(rawt)
      
    elif ext == 'pdf':
      rawt = read_pdf(prompt)
      
    else:
      console.status("File format not supported: "+ext)
      exit()
    return pro

def get_fun_def(func):

    for file in os.listdir(os.path.dirname(__file__)+"/functions"):
      if file.endswith(".py"):
        file_name = file[:-3]
        module_name = 'functions.' + file_name
        for name, cls in inspect.getmembers(importlib.import_module(module_name), inspect.isclass):
          if cls.__module__ == module_name:
           if func in dir(cls):
            obj = cls()
            full = inspect.getfullargspec(getattr(obj, func))
            args = ', '.join(full.args)
            available_functions[func] = getattr(obj, func)
            available_parameters[func] = full.args
            available_descr[func] = obj.functions
            return available_descr[func][0]
    return ""

def print_url_list(heading, responce):
    console.print(heading)
    row = 1
    for url in responce.data:
      console.print(Markdown("  [url " + str(row) + "](" + url["url"] + ")"))
    

def main():
    desc = "This tool sends a query to OpenAIs Chat API from the command line.\n\n"\
           "A new chat session is started with -n <pre-info> and gives the opportunity to\n"\
           "provide pre-information to your question\n\n"\
           "Report any issues at: https://github.com/draupner1/oai/issues"
    epilog = "Please note that the responses from OpenAI's API are not guaranteed to be accurate and " \
            "use of the tool is at your own risk.\n"
    numb = 2

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(prog='oai - CLI assistant',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description=desc,
                                     epilog=epilog)

      
    # Add arguments for expert mode, API key reset, version, and prompt
    parser.add_argument('-c', '--create', action="store_true", help='Create a new Image, DALL-E3', dest='create')
    parser.add_argument('-w', '--variant', action="store_true", help='Create a variant of an Image-file. Provide "<image.png>", DALL-E2', dest='variant')
    parser.add_argument('-e', '--edit', action="store_true", help='Edit part of an Image-file. Provide "<image.png>,<mask.png>, Prompt-string",DALL-E2', dest='edit')
    parser.add_argument('-d', '--default', default=2, help='How many Images to create. default=2', dest='default')
    parser.add_argument('-s', '--size', default="1024x1024", help='Image size. default=1024x1024', dest='size')
    
    parser.add_argument('-n', '--new', action="store_true", help='Start New Chat', dest='new')
    parser.add_argument('-f', '--function', default='', help='Enable function call', dest='function')
 #   parser.add_argument('name', nargs='?', default="")
    parser.add_argument('-l', '--linux', action="store_true", help='Include an assistent message with Kernel/OS/shell', dest='linux')
    parser.add_argument('-m', '--model', action="store_true", help='List models available via OpenAIs API', dest='model')
    parser.add_argument('-x', '--expert', action="store_true", help='Toggle warning', dest='expert')
    parser.add_argument('-i', '--key', action="store_true", help='Reset API key', dest='apikey')
    parser.add_argument('-v', '--version', action="store_true", help=f'Get Version (hint: it\'s {version})', dest='version')
    parser.add_argument('--licenses', action="store_true", help='Show oai & Third Party Licenses', dest='licenses')
    parser.add_argument('prompt', type=str, nargs='?', help='Prompt to send')
    args = parser.parse_args()

    if args.default:
      numb = int(args.default)

    if args.new:
        console.status("Starting a new chat session")
        if os.path.exists(_session_file_):
          os.remove(_session_file_)
        if args.prompt:
          prompt = args.prompt
          if os.path.exists(prompt):
            prompt = extract_jsonstr(prompt)
        else:
          prompt = ""
        pprompt = f"{prompt}\n\n" \
                  f"Response Format: Markdown\n"
        messages=[{'role':'assistant', 'content':pprompt}]
        put_session(messages)
        sys.exit()
 
    if args.linux:
        prompt = get_lindata()
        if os.path.isfile(_session_file_):
          messages=get_session()
          messages.append({'role':'user', 'content':prompt})
        else:
          messages=[{'role':'user', 'content':prompt}]
        put_session(messages)  
        sys.exit()
 
    if args.model:
        model_list = get_models()
        for mod in model_list:
          print(mod['id'])
        sys.exit()

    if args.version:
        console.print("oai version: " + version)
        sys.exit()
 
    if args.licenses:
        # print LICENSE file with pagination
        with console.pager():
            try:
                with open("LICENSE", "r") as f:
                    console.print(f.read())
            except FileNotFoundError:
                with open("/app/bin/LICENSE", "r") as f:
                    console.print(f.read())
        sys.exit()

    config.check_config(console)
    if args.apikey:
        config.prompt_new_key()
        sys.exit()

    if args.expert:
        config.toggle_expert_mode()
        sys.exit()

    func = ""
    if args.function:
        func = args.function
        if func == "":
            print("No function provided. Exiting...")
            sys.exit()
        func = get_fun_def(func)
        if func == "":
            print('Function not found: ' + func)
            sys.exit()

    if not args.prompt:
        prompt = Prompt.ask("Documentation Request")
        if prompt == "":
            print("No prompt provided. Exiting...")
            sys.exit()
    else:
        prompt = args.prompt
    askDict = {'role':'user', 'content':prompt}
    if os.path.isfile(_session_file_):
      messages = get_session()
      messages.append(askDict)
    else:
      messages=[askDict]

    if args.create:
      if args.size not in ["1024x1024", "1792x1024", "1024x1792"]:
        print('DALL-E3 only supports, "1024x1024", "1792x1024", "1024x1792"')
        print("size: " + args.size)
        exit()
      with console.status(f"Phoning a friend...  ", spinner="pong"):
        print('Doing an image')
        openai_response = get_image(prompt, numb, args.size)
       # print(openai_response)
        print_url_list("Created links:", openai_response)
        exit()

    if args.variant:
      with console.status(f"Phoning a friend...  ", spinner="pong"):
        print('Variant of an image: ' + prompt)
        openai_response = get_variant(prompt, numb)
       # print(openai_response)
        print_url_list("Variant links:", openai_response)
        exit()

    if args.edit:
      with console.status(f"Phoning a friend...  ", spinner="pong"):
        print('Edit of an image: ' + prompt)
        openai_response = get_edit(prompt, numb)
       # print(openai_response)
        print_url_list("Edited links:", openai_response)
        exit()

    with console.status(f"Phoning a friend...  ", spinner="pong"):
        openai_response = get_chat(messages, func)
        if openai_response.get("function_call"):
          function_name = openai_response["function_call"]["name"]
          if function_name in available_functions:
            fuction_to_call = available_functions[function_name]
          else:
            print('Bad returned function name from OpenAI API')
            print(openai_response)
            messages.append(openai_response)
            messages.append({"role": "function", "name": function_name, "content": func})
            function_args = json.loads(openai_response["function_call"]["arguments"].strip())
            console.print(Markdown(function_args.get("content").strip()))
            put_session(messages)
            exit()

          #print(openai_response["function_call"]["arguments"].strip())
          function_args = json.loads(openai_response["function_call"]["arguments"].strip())
          #print("Function arguments")
          #print(function_args)
          function_response = fuction_to_call(
            **function_args
          )
          messages.append(openai_response)
          messages.append({"role": "function", "name": function_name, "content": function_response})

          if function_response != 'stop':
            openai_response = get_chat(messages)
          else:
            openai_response.content = function_args.get("content")
        console.print(Markdown(openai_response.content.strip()))
        messages.append({'role':'assistant', 'content':openai_response.content.strip()})
        put_session(messages)


if __name__ == "__main__":
    main()
