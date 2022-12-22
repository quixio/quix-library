from quixstreaming import QuixStreamingClient, StreamEndType, StreamReader, ParametersBufferConfiguration
from quixstreaming.app import App
from threshold_function import ThresholdAlert
import os

# Quix injects credentials automatically to the client. Alternatively, you can always pass an SDK token manually as an argument.
client = QuixStreamingClient()

# Change consumer group to a different constant if you want to run model locally.
print("Opening input and output topics")

# Environment variables
input_topic = client.open_input_topic(os.environ["input"], "default-consumer-group")
output_topic = client.open_output_topic(os.environ["output"])

bufferMilliSeconds = os.environ["bufferMilliSeconds"]
if isinstance(bufferMilliSeconds, int):
    msecs = int(bufferMilliSeconds)
else:
    raise Exception("bufferMilliSeconds should be an integer")

# Callback called for each incoming stream
def read_stream(input_stream: StreamReader):
    # Create a new stream to output data
    output_stream = output_topic.create_stream(input_stream.stream_id + '-' + os.environ["Quix__Deployment__Name"])
    output_stream.properties.parents.append(input_stream.stream_id)

    # handle the data in a function to simplify the example
    quix_function = ThresholdAlert(input_stream, output_stream)

    buffer_options = ParametersBufferConfiguration()
    buffer_options.time_span_in_milliseconds = msecs
    buffer = input_stream.parameters.create_buffer()

    # React to new data received from input topic.
    buffer.on_read_pandas += quix_function.on_pandas_frame_handler

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
