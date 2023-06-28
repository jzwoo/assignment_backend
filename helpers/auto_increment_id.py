from pymongo.errors import AutoReconnect
from config.db import db


def get_next_sequence_value(counter_name):
    counters_collection = db['counters']

    try:
        counter = counters_collection.find_one_and_update(
            {'_id': counter_name},
            {'$inc': {'count': 1}},
            projection={'count': True},
            upsert=True,
            return_document=True
        )

        return counter['count']
    except AutoReconnect:
        # Handle connection errors if needed
        pass
