import sys

import openai

from resources import config

def get_completion(prompt):
    openai.api_key = config.get_api_key()
    engine = config.get_model()

    if prompt is None:
        print("Prompt is empty. Please enter a prompt.")

    # token calculator
    # count characters in prompt
    tokens_prompt = len(prompt) / 4
    max_tokens = int(4000 - tokens_prompt)
    # print(f"Max tokens: {max_tokens}")
    # print(f"Tokens in prompt: {tokens_prompt}")
    try:
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        ).choices[0].text
    except openai.error.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        sys.exit()
    except openai.error.APIConnectionError as e:
        # Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        sys,exit()
    except openai.error.RateLimitError as e:
        # Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        sys.exit()
    except openai.error.OpenAIError as e:
        print(f"OpenAI API returned an error: {e}")
        sys.exit()
    return response
    
def get_chat(messages, func = ""):
    openai.api_key = config.get_api_key()
    engine = config.get_model()

    if len(messages) == 0:
        print("Prompt is empty. Please enter a prompt.")

    try:
        if func == "":
          response = openai.ChatCompletion.create(
              model=engine,
              messages=messages
          ).choices[0].message
        else:
          response = openai.ChatCompletion.create(
              model=engine,
              messages=messages,
              functions=[func]
          ).choices[0].message
    except openai.error.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        sys.exit()
    except openai.error.APIConnectionError as e:
        # Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        sys,exit()
    except openai.error.RateLimitError as e:
        # Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        sys.exit()
    except openai.error.OpenAIError as e:
        print(f"OpenAI API returned an error: {e}")
        sys.exit()
    return response
    
def get_models():
    openai.api_key = config.get_api_key()
#    engine = config.get_model()

    try:
        response = openai.Model.list(
        ).data
    except openai.error.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        sys.exit()
    except openai.error.APIConnectionError as e:
        # Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        sys,exit()
    except openai.error.RateLimitError as e:
        # Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        sys.exit()
    except openai.error.OpenAIError as e:
        print(f"OpenAI API returned an error: {e}")
        sys.exit()
    return response
    
def get_image(prompt, num, size):
    if num<1 or num>10:
      print("Number of variants to generate must be between 1 to 10")
      exit()
    openai.api_key = config.get_api_key()
    try:
        response = openai.Image.create(
                   prompt = prompt,
                   n = num,
                   size=size,
                   model="dall-e-3"
                   )
    except openai.error.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        sys.exit()
    except openai.error.APIConnectionError as e:
        # Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        sys,exit()
    except openai.error.RateLimitError as e:
        # Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        sys.exit()
    except openai.error.OpenAIError as e:
        print(f"OpenAI API returned an error: {e}")
        sys.exit()
    return response


def get_variant(prompt, num):
    if num<1 or num>10:
      print("Number of variants to generate must be between 1 to 10")
      exit()
    try:
      open(prompt, "rb")
    except OSError:
      print("Missing Imagefile in this directory")
      exit()
    openai.api_key = config.get_api_key()
    try:
        response = openai.Image.create_variation(
                   image = open(prompt, "rb"),
                   n = num,
                   size="1024x1024"
                   )
    except openai.error.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        sys.exit()
    except openai.error.APIConnectionError as e:
        # Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        sys,exit()
    except openai.error.RateLimitError as e:
        # Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        sys.exit()
    except openai.error.OpenAIError as e:
        print(f"OpenAI API returned an error: {e}")
        sys.exit()
    return response

def get_edit(prompt, num):
    if num<1 or num>10:
      print("Number of variants to generate must be between 1 to 10")
      exit()
    pl = prompt.split(',')
    if len(pl) < 3:
      print("Prompt must contain <img.png>,<mask.png>,The new image prompt")
      exit()
    try:
      open(pl[0], "rb")
    except OSError:
      print("Missing Imagefile in this directory")
      exit()
    try:
      open(pl[1], "rb")
    except OSError:
      print("Missing Maskfile in this directory")
      exit()
    openai.api_key = config.get_api_key()
    img = pl[0]
    msk = pl[1]
    prt = ' '.join(pl[2:])
#    print( img )
#    print( msk )
#    print( prt )
    try:
        response = openai.Image.create_edit(
                   image = open(img, "rb"),
                   mask = open(msk, "rb"),
                   prompt = prt,
                   n = num,
                   size="1024x1024"
                   )
    except openai.error.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        sys.exit()
    except openai.error.APIConnectionError as e:
        # Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        sys,exit()
    except openai.error.RateLimitError as e:
        # Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        sys.exit()
    except openai.error.OpenAIError as e:
        print(f"OpenAI API returned an error: {e}")
        sys.exit()
    return response

