def block_duration(block):

    if block.end_hour > block.start_hour:
        return block.end_hour - block.start_hour

    return (24 - block.start_hour) + block.end_hour