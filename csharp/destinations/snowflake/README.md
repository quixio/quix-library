# Snowflake Sink

Stream data from Quix to Snowflake, it handles both parameter and event data.

## Requirements / Prerequisites
 - A Snowflake account.

## Environment variables

The code sample uses the following environment variables:

- **Broker__TopicName**: Name of the input topic to read from.
- **Snowflake__Locator**: Locator of the account. Can be found under Admin/Accounts or in the URL.
- **Snowflake__Region**: Region of the account. Can be found under Admin/Accounts or in the URL.
  - e.g.: west-europe.azure. 
  - note: display name is used on Accounts page, but locator lets you copy the one needed. It should have the format of `https://{locator}.{region}.snowflakecomputer.com`
- **Snowflake__Database**: The name of the database to persist to      
- **Snowflake__User**: The username of the user the sink should use to interact with the database.
- **Snowflake__Password**: The password of the user configured above.

## Known limitations 
- Binary parameters are not supported in this version

## Docs
Check out the [SDK docs](https://docs.quix.io/sdk-intro.html) for detailed usage guidance

## How to run
Create an account on [Quix](https://portal.platform.quix.ai/self-sign-up?xlink=github) to edit or deploy this application without a local environment setup.
