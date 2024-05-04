import sys
import requests
import json
import subprocess
from resources import config

class ConduOll:
  def __init__(self):
    self.model = config.get_oll_model()
    self.port = config.get_oll_port()
                
  def get_chat(this, messages):

    if len(messages) == 0:
        print("Prompt is empty. Please enter a prompt.")
        exit()

    try:
        url = "http://localhost:" + this.port + "/api/chat"
        #url = "http://127.0.0.1:" + this.port + "/api/chat"
        data = { "model": this.model,
                 "stream" : False,
                 "messages": messages }
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()
        jresp = resp.json()
    except requests.exceptions.RequestException as e:  # This is the correct syntax
      raise SystemExit(e)
    return jresp['message']

    
  def get_models(this):
    
    try:
        subprocess.run(["ollama", "list"], subprocess.STDOUT) #capture_output=True)
    except OSError as e:
        # Handle API error here, e.g. retry or log
        print(f"OS Error: {e}")
        sys.exit()
    except ValueError as e:
        # Handle connection error here
        print(f"Value Error: {e}")
        sys,exit()
    response = []
    return response
    


