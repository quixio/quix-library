from quixstreaming import QuixStreamingClient, StreamEndType, StreamReader
from quixstreaming.app import App
from percentage_function import PercentageAlert
import os

# Quix injects credentials automatically to the client. Alternatively, you can always pass an SDK token manually as an argument.
client = QuixStreamingClient()

# Change consumer group to a different constant if you want to run model locally.
print("Opening input and output topics")

# Define environmental variables
input_topic = client.open_input_topic(os.environ["input"], "default-consumer-group")
output_topic = client.open_output_topic(os.environ["output"])


# Callback called for each incoming stream
def read_stream(input_stream: StreamReader):
    # Create a new stream to output data
    output_stream = output_topic.create_stream(input_stream.stream_id + '-' + os.environ["Quix__Deployment__Name"])
    output_stream.properties.parents.append(input_stream.stream_id)

    # handle the data in a function to simplify the example
    perc_alert = PercentageAlert(consumer_stream, producer_stream)

    # React to new data received from input topic.
    consumer_stream.timeseries.on_dataframe_received = perc_alert.on_data_frame_handler

    # When input stream closes, we close output stream as well. 
    def on_stream_close(end_type: StreamEndType):
        output_stream.close()
        print("Stream closed:" + output_stream.stream_id)

    input_stream.on_stream_closed += on_stream_close


# Hook up events before initiating read to avoid losing out on any data
input_topic.on_stream_received += read_stream

# Hook up to termination signal (for docker image) and CTRL-C
print("Listening to streams. Press CTRL-C to exit.")

# Handle graceful exit of the model.
App.run()
