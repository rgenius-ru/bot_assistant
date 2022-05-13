def shorten_list(source_list, max_count=10, head_count=5, tail_count=5):
    if len(source_list) > max_count:
        return source_list[:head_count] + ['...'] + source_list[-tail_count:]

    return source_list
