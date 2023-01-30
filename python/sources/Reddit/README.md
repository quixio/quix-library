# A Reddit Source 
Integrate a Reddit feed into your Quix pipeline

## Requirements/prerequisites

You will need to create a Reddit App [here](https://www.reddit.com/prefs/apps). 

Steps:
- Provide a name
- Choose 'script'
- Provide a description
- Provide a 'redirect uri'
- Click 'create app'

Now you can use the 'client id' and 'secret' to configure the Reddit connector.

![graph](reddit_app.png?raw=true)

## Environment variables

The code sample uses the following environment variables:

- **output**: Name of the output topic to write data into.
- **reddit_username**: The Reddit user name to use.
- **reddit_password**: The password to use.
- **reddit_client_id**: The Reddit client id (shown under the app name).
- **reddit_client_secret**: The reddit secret (shown after creating the app in Reddit).
- **subreddit**: The sub Reddit to scrape.

## Docs

Check out the [SDK docs](https://quix.io/docs/sdk/introduction.html) for detailed usage guidance.

## How to run
Create a [Quix](https://portal.platform.quix.ai/self-sign-up?xlink=github) account to edit or deploy this application without a local environment setup.

Alternatively, you can learn how to set up your local environment [here](https://quix.io/docs/sdk/python-setup.html).
