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