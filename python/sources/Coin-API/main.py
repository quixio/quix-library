import quixstreams as qx
from quix_functions import QuixFunctions
import requests
import time
import traceback
from threading import Thread
import os

try:
    # should the main loop run?
    run = True

    # Quix injects credentials automatically to the client.
    # Alternatively, you can always pass an SDK token manually as an argument.
    client = qx.QuixStreamingClient()

    # Open the output topic where to write data out
    print("Opening output topic")
    producer_topic = client.get_topic_producer(os.environ["output"])

    # Which currency pairs are you interested in?
    primary_currency = os.environ["primary_currency"]  # e.g."BTC"
    secondary_currencies = os.environ["secondary_currencies"]  # e.g."USD,GBP"

    url = 'https://rest.coinapi.io/v1/exchangerate/{0}?filter_asset_id={1}'.format(primary_currency, secondary_currencies)

    # COIN API Key
    coin_api_key = "{}".format(os.environ["coin_api_key"])

    if coin_api_key == '':
        raise ValueError('Please update coin_api_key env var with your COIN API Key')

    headers = {'X-CoinAPI-Key': coin_api_key}

    stream_producer = producer_topic.create_stream("coin-api")

    # Give the stream human-readable name. This name will appear in data catalogue.
    stream_producer.properties.name = "Coin API"

    # Save stream in specific folder in data catalogue to help organize your workspace.
    stream_producer.properties.location = "/Coin API"


    def get_data():
        global run

        quix_functions = QuixFunctions(stream_producer)

        while run:
            response = requests.get(url, headers = headers)

            data = response.json()

            rows = data['rates']

            quix_functions.data_handler(rows, primary_currency)

            # We sleep for 15 minutes so we don't reach free COIN API account limit.
            # Stop sleeping if process termination requested
            sleeping = 0
            while sleeping <= 900 and run:
                sleeping = sleeping + 1
                time.sleep(1)


    def before_shutdown():
        global run

        # Stop the main loop
        run = False


    def main():
        thread = Thread(target = get_data)
        thread.start()

        print("CONNECTED!")

        qx.App.run(before_shutdown = before_shutdown)

        # wait for worker thread to end
        thread.join()

        print("Exiting")


    if __name__ == "__main__":
        main()

except Exception:
    print("ERROR: {}".format(traceback.format_exc()))
