MAX_MESSAGE_LEN = 4096


def max_message_len(text):
    return len(text) > MAX_MESSAGE_LEN


def text_split_message(text):
    if max_message_len(text):
        return [text[i:i + MAX_MESSAGE_LEN] for i in range(0, len(text), MAX_MESSAGE_LEN)]
    return [text]
