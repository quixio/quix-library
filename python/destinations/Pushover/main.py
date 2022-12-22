from quixstreaming import QuixStreamingClient, StreamReader
from quixstreaming.app import App
from quix_function import QuixFunction
import os

# Quix injects credentials automatically to the client.
# Alternatively, you can always pass an SDK token manually as an argument.
client = QuixStreamingClient()

print("Opening input and output topics")
input_topic = client.open_input_topic(os.environ["input"], "default-consumer-group-5")


# Callback called for each incoming stream
def read_stream(input_stream: StreamReader):

    # Create a new stream to output data
    # handle the data in a function to simplify the example
    quix_function = QuixFunction(input_stream)
        
    # React to new data received from input topic.
    input_stream.parameters.on_read_pandas += quix_function.on_pandas_frame_handler
    input_stream.events.on_read += quix_function.on_event_data_handler


# Hook up events before initiating read to avoid losing out on any data
input_topic.on_stream_received += read_stream

# Hook up to termination signal (for docker image) and CTRL-C
print("Listening to streams. Press CTRL-C to exit.")

# Handle graceful exit of the model.
App.run()
