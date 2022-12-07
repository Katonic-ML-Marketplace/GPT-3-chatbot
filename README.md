# GPT-3-chatbot

Here we build a simple chatbot that knows about a specific topic that you provide as prompt. Users can naturally chat with the bot through the app, asking whatever they want. When the questions refer to the topic you informed the chatbot with, then it will reply based on that content.

## OpenAI GPT-3 API Access

Signup to the [OpenAI](https://openai.com/api/) in order to obtain access to the GPT-3 API.
Once you have the API, generate your secret key and export it as an environment variable.

```
export OPENAI_KEY="xxxxxxxxxxx"
```
Where "xxxxxxxxxxx" corresponds to your secret key.

## Run the Chatbot App

clone the repo

```
https://github.com/Katonic-ML-Marketplace/GPT-3-chatbot.git
```
Install all the requirements

```
pip install -r requirements.txt
```

Run the app
```
python app.py
```