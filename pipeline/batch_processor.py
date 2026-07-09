"""
Batch Processor
"""

from itertools import islice


def batch_generator(images, batch_size=100):

    iterator = iter(images)

    while True:
        batch = list(islice(iterator, batch_size))

        if not batch:
            break

        yield batch


# UNUSED
# def chunk_list(items, chunk_size):
#     items = list(items)
#     return [
#         items[i:i + chunk_size]
#         for i in range(0, len(items), chunk_size)
#     ]
