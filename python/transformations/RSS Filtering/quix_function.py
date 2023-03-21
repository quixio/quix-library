import quixstreams as qx
import traceback
import os


class QuixFunction:
    def __init__(self, consumer_stream: qx.StreamConsumer, producer_stream: qx.StreamProducer):
        self.consumer_stream = consumer_stream
        self.producer_stream = producer_stream

    # Callback triggered for each new parameter data.
    def on_parameter_data_handler(self, stream_consumer: qx.StreamConsumer, data: qx.TimeseriesData):
     
        # get the value for the filter
        tag_filter = os.environ["tag_filter"]

        for timestamp in data.timestamps:
            # get the tag string. it's an array of objects
            tag_string = timestamp.parameters['tags'].string_value
            # convert the string to an array. this is dangerous and needs error handling
            o = eval(tag_string)
            # loop through the objects in the list
            # get the value for the "term" element
            tags = [x["term"] for x in o]
            # make these into a list for display later
            tags_list = ", ".join(tags)
            
            # it should be a comma seperated list, so split it
            filters_terms = [x.strip() for x in tag_filter.split(',')]

            print(filters_terms)

            for tag in tags:
                try:
                    if tag in filters_terms: 
                        print("YAY '{}' matches the filter".format(tag))
                        
                        # if you want to augment the data further add more lines here
                        data.timestamps[0].add_value("FILTERED", "True")
                        data.timestamps[0].add_value("TAG_MATCH", tag)
                        data.timestamps[0].add_value("TAGS_LIST", tags_list)
                        self.producer_stream.timeseries.buffer.publish(data)  # Send filtered data to output topic
                    # else:
                    #     print("{} not found in the filters :-(".format(filter_term))
                except Exception:
                    print(traceback.format_exc())


