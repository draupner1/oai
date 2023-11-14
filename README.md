oai - Ask question from bash shell and get tailored documentation response 
========================================
![image](https://user-images.githubusercontent.com/3023775/232043126-34d4fcae-65d8-449a-9738-7f9726f55d11.png)

oai is a command line tool that uses OpenAI's language model to provide a documentation-like experience to users. With oai, users can get answers to their questions and receive step-by-step guidance to complete tasks.


<details>
  <summary>Get API Key from OpenAI</summary>

1.  Get your OpenAI API Key:
2.  Go to OpenAI's website ([https://openai.com/api/login](https://openai.com/api/login))
3.  Sign up or log in to your account
4.  Go to the API Key section ([https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys))
5.  Create a new secret key
6.  Copy the API key
7.  When running oai the first time, you will be prompted for your key
  
</details>

( Anyone who might be able to help me get this set up with a snap or flatpack? I've been working on trying to set up these workflows )

Quick Start
-----------

1. Clone repository `git clone https://github.com/draupner1/oai.git'
2. Change directory `cd oai`
3. Install dependencies `pip install -r requirements.txt`
4. Run `python oai` and enter OpenAI key as prompted to complete setup
5. Prompt with `python oai` or `python oai "how do I..."` 
6. Optional: Install link in PATH, or in ~/.local/bin/
<details>
  <summary>Python Requirements</summary>

*   Python 3
*   OpenAI API Key
*   Rich library (install via `pip install rich`)

</details>

Usage
-----

To use oai, simply run the script and provide a prompt that describes the task you want to complete or the question you want to ask.

For example:

`python oai.py "How to install and run a web server on Ubuntu?"`

If you have added the script to your path, you can run it from anywhere:

`oai "How to install and run a web server on Ubuntu?"`

![image](https://user-images.githubusercontent.com/3023775/232043124-5bcdc240-4b86-4397-9355-ff0a8dc2f3fe.png)
![image](https://user-images.githubusercontent.com/3023775/232043119-d25b1e93-c99b-48e6-b9c6-ccbc1270a800.png)

New openAI lib v 1.2
--------------------
On new installs after Nov6-23 we get the new python lib v 1.2.

This breaks some calls and responce types.

OAI v.0.6.1 is adapted to the new lib!

Also, providing new shortcuts for -s size when generating Images.
Use '1:1', '16:9', '9:16' as shorthand for '1024x1024' and...

Also-2, when generating images, printing the returned eventually altered prompt.


Image Generation
----------------
Available from v.0.6.0
As the API provides, creation -c is DALL-E3,
Variants and Edit are DALL-E2.

  -c, --create          Create a new Image, DALL-E3
  -w, --variant         Create a variant of an Image-file. Provide "<image.png>", DALL-E2
  -e, --edit            Edit part of an Image-file. Provide "<image.png>,<mask.png>, Prompt-string",DALL-E2
  -d DEFAULT, --default DEFAULT
                        How many Images to create. 1-10, default=2
  -s SIZE, --size SIZE  Image size. default=1024x1024

Will respond with clickable link (that expires) to be opened in Browser.

Plug-ins
--------
Available from v.0.5.0

You can now define your own Functions. (See OpenAI-chatAPI for details)

Implement them in a Class file, and drop it in the functions directory where OAI is installed.

Your functions/FuncTemplate.txt, is a class template to get you started.

Options
-------

* If you wish, you can override automated settings by use of .env file
* You can set the OpenAI model to use by setting the `OPENAI_MODEL` environment variable in your .env file.
* You can disable the notice that is displayed at the end of the response by setting the `OPENAI_DISABLE_NOTICE` environment variable in your .env file.

Contributing
------------

If you'd like to contribute to oai, feel free to create a pull request or open an issue. All contributions are welcome!
